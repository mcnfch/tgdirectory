#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
PLACES_API_URL = 'https://places.googleapis.com/v1/places:searchText'
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Results')

# Fields we want to collect that are unique to Google Places
# Excluding fields we already have from Foursquare:
# - name (displayName)
# - address (formattedAddress)
# - location (lat/lng)
# - phone
# - website
# - hours
# - rating
# - price level
FIELD_MASK = ','.join([
    'places.id',
    'places.googleMapsUri',
    'places.businessStatus',
    'places.photos',
    'places.userRatingCount',
    # Dining-specific fields not in Foursquare
    'places.servesBreakfast',
    'places.servesBrunch',
    'places.servesLunch',
    'places.servesDinner',
    'places.servesVegetarianFood',
    'places.servesCocktails',
    'places.servesBeer',
    'places.servesWine',
    'places.servesCoffee',
    'places.servesDessert',
    'places.dineIn',
    'places.outdoorSeating',
    'places.reservable',
    'places.goodForChildren',
    'places.goodForGroups',
    'places.liveMusic',
    'places.delivery',
    'places.takeout',
    'places.curbsidePickup',
    'places.parkingOptions',
    'places.restroom',
    'places.paymentOptions'
])

def ensure_results_dir():
    """Ensure the Results directory exists"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

def load_foursquare_data(filename='restaurant_results.json'):
    """Load restaurants from our Foursquare results"""
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Results', filename)
    print(f"Loading data from: {filepath}")
    with open(filepath, 'r') as f:
        data = json.load(f)
        restaurants = []
        for city in data['cities']:
            for restaurant in city['restaurants']:
                restaurants.append({
                    'name': restaurant['name'],
                    'address': restaurant['address'],
                    'city': city['city'],
                    'state': city['state'],
                    'latitude': restaurant.get('latitude', city['coordinates']['latitude']),
                    'longitude': restaurant.get('longitude', city['coordinates']['longitude'])
                })
        return restaurants

def transform_to_schema(place_data, foursquare_data):
    """Transform Google Places API data to match our schema, combining with Foursquare data"""
    if not place_data:
        return None
        
    return {
        "google_data": {
            "id": place_data.get('id', ''),
            "googleMapsUri": place_data.get('googleMapsUri', ''),
            "businessStatus": place_data.get('businessStatus', ''),
            "userRatingCount": place_data.get('userRatingCount', 0),
            "photos": [photo.get('name', '') for photo in place_data.get('photos', [])],
            "foodOptions": {
                "servesBreakfast": place_data.get('servesBreakfast', False),
                "servesBrunch": place_data.get('servesBrunch', False),
                "servesLunch": place_data.get('servesLunch', False),
                "servesDinner": place_data.get('servesDinner', False),
                "servesVegetarianFood": place_data.get('servesVegetarianFood', False),
                "servesCocktails": place_data.get('servesCocktails', False),
                "servesBeer": place_data.get('servesBeer', False),
                "servesWine": place_data.get('servesWine', False),
                "servesCoffee": place_data.get('servesCoffee', False),
                "servesDessert": place_data.get('servesDessert', False)
            },
            "diningExperience": {
                "dineIn": place_data.get('dineIn', False),
                "outdoorSeating": place_data.get('outdoorSeating', False),
                "reservable": place_data.get('reservable', False),
                "goodForChildren": place_data.get('goodForChildren', False),
                "goodForGroups": place_data.get('goodForGroups', False),
                "liveMusic": place_data.get('liveMusic', False)
            },
            "convenience": {
                "delivery": place_data.get('delivery', False),
                "takeout": place_data.get('takeout', False),
                "curbsidePickup": place_data.get('curbsidePickup', False),
                "parkingOptions": place_data.get('parkingOptions', ''),
                "restroom": place_data.get('restroom', False),
                "paymentOptions": place_data.get('paymentOptions', [])
            }
        },
        "foursquare_data": foursquare_data
    }

def search_place(restaurant):
    """Search for a place using restaurant name and location"""
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': FIELD_MASK
    }
    
    # Create a specific query using name, city, and state
    query = f"{restaurant['name']} in {restaurant['city']}, {restaurant['state']}"
    
    data = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": float(restaurant.get('latitude', 0)),
                    "longitude": float(restaurant.get('longitude', 0))
                },
                "radius": 5000.0  # 5km radius
            }
        }
    }
    
    try:
        response = requests.post(PLACES_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching for {restaurant['name']}: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

def main():
    # Ensure Results directory exists
    ensure_results_dir()
    
    # Load restaurants from Foursquare data
    restaurants = load_foursquare_data()
    print(f"Loaded {len(restaurants)} restaurants from Foursquare data\n")
    
    # Process restaurants
    results = []
    total = len(restaurants)
    
    for i, restaurant in enumerate(restaurants, 1):
        name = restaurant['name']
        print(f"\nProcessing {i}/{total}: {name} in {restaurant['city']}, {restaurant['state']}")
        
        place_data = search_place(restaurant)
        if place_data and 'places' in place_data and place_data['places']:
            transformed_data = transform_to_schema(place_data['places'][0], restaurant)
            if transformed_data:
                results.append(transformed_data)
                print(f"Found and transformed data for: {name}")
        else:
            print(f"Could not find place data for: {name}")
        
        # Add delay between requests to respect rate limits
        # Adjust this based on your API quota
        time.sleep(2)
        
        # Save progress every 50 restaurants
        if i % 50 == 0:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            progress_file = os.path.join(RESULTS_DIR, f'places_api_progress_{timestamp}.json')
            with open(progress_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nProgress saved: {len(results)} restaurants to {progress_file}")
    
    # Save final results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(RESULTS_DIR, f'combined_restaurant_data_{timestamp}.json')
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_restaurants': len(results),
            'restaurants': results
        }, f, indent=2)
    print(f"\nSaved {len(results)} restaurants to {output_file}")

if __name__ == '__main__':
    main()
