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

PLACES_API_URL = 'https://places.googleapis.com/v1/places:searchText'
RESULTS_DIR = '/opt/noogabites/Results'

# Fields we want to collect that are unique to Google Places
# Note: We collect some overlapping fields from both APIs
# to ensure data completeness and cross-validation
FIELD_MASK = ','.join([
    'places.id',
    'places.googleMapsUri',
    'places.businessStatus',
    'places.photos',
    'places.userRatingCount',
    'places.displayName',
    'places.formattedAddress',
    'places.location',
    'places.internationalPhoneNumber',
    'places.websiteUri',
    'places.regularOpeningHours',
    'places.rating',
    'places.priceLevel',
    # Dining-specific fields
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
    'places.wheelchairAccessibleParking',
    'places.wheelchairAccessibleEntrance'
])

def ensure_results_dir():
    """Ensure the Results directory exists"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

def load_foursquare_data(filename='restaurant_differential.json'):
    """Load restaurants from our Foursquare results"""
    filepath = os.path.join(RESULTS_DIR, filename)
    print(f"Loading data from: {filepath}")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Extract restaurants from the differential file
    restaurants = data.get('restaurants', [])
    print(f"Found {len(restaurants)} restaurants")
    return restaurants

def transform_to_schema(place_data):
    """Transform the place data to match our schema"""
    if not place_data or 'places' not in place_data or not place_data['places']:
        return None
    
    place = place_data['places'][0]
    
    # Extract photo references if available
    photos = []
    if 'photos' in place:
        photos = [photo['name'] for photo in place['photos']]
    
    # Extract city from formatted address
    address = place.get('formattedAddress', '')
    city = ''
    if address:
        # Address format is typically: street, city, state zip
        parts = address.split(',')
        if len(parts) >= 2:
            city = parts[1].strip()
            # Remove state and zip if present
            city = city.split()[0]
    
    # Map Google place types to categories
    type_to_category = {
        'restaurant': 'Restaurant',
        'food': 'Restaurant',
        'cafe': 'Cafe',
        'bar': 'Bar',
        'meal_takeaway': 'Fast Food Restaurant',
        'meal_delivery': 'Restaurant',
        'bakery': 'Bakery',
        'american_restaurant': 'American Restaurant',
        'chinese_restaurant': 'Chinese Restaurant',
        'mexican_restaurant': 'Mexican Restaurant',
        'italian_restaurant': 'Italian Restaurant',
        'japanese_restaurant': 'Japanese Restaurant',
        'thai_restaurant': 'Thai Restaurant',
        'indian_restaurant': 'Indian Restaurant',
        'steakhouse': 'Steakhouse',
        'seafood_restaurant': 'Seafood Restaurant',
        'fast_food_restaurant': 'Fast Food Restaurant',
        'pizza_restaurant': 'Pizzeria',
        'barbecue_restaurant': 'BBQ Joint',
        'burger_restaurant': 'Burger Joint'
    }
    
    categories = []
    for place_type in place.get('types', []):
        if place_type in type_to_category:
            category = type_to_category[place_type]
            if category not in categories:
                categories.append(category)
    
    # If no categories mapped, add 'Restaurant' as default
    if not categories:
        categories = ['Restaurant']
    
    result = {
        'name': place.get('displayName', {}).get('text', ''),
        'categories': categories,
        'address': address,
        'city': city,
        'state': 'TN',  # Default to TN since we're focusing on Chattanooga area
        'postal_code': '',  # We could extract this from address if needed
        'country': 'US',
        'phone': place.get('nationalPhoneNumber', ''),
        'website': place.get('websiteUri', ''),
        'hours': {},  # Places API doesn't provide hours in basic data
        'rating': place.get('rating', 0),
        'review_count': place.get('userRatingCount', 0),
        'price_level': place.get('priceLevel', ''),
        'delivery': False,  # Default values since Places API doesn't provide these
        'takeout': False,
        'reserve': False,
        'photos': photos,
        'google_place_id': place.get('id', '')
    }
    
    return result

def save_results(results):
    """Save results to a JSON file"""
    output_file = os.path.join(RESULTS_DIR, 'google_places_results.json')
    
    # Create the same structure as merged data
    output_data = {
        'restaurants': results
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Saved {len(results)} results to {output_file}")

def search_place(name, address):
    """Search for a place using restaurant name and location"""
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,places.types,places.websiteUri,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.priceLevel,places.photos.name,places.photos.widthPx,places.photos.heightPx'
    }
    
    # Create a specific query using name and address
    query = f"{name} {address}"
    
    data = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": 35.0456,  # Chattanooga latitude
                    "longitude": -85.3097  # Chattanooga longitude
                },
                "radius": 50000.0  # 50km radius
            }
        },
        "languageCode": "en"
    }
    
    try:
        response = requests.post(PLACES_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching for {name}: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main function to run the script"""
    # Load restaurants from Foursquare data
    restaurants = load_foursquare_data()
    if not restaurants:
        print("No restaurants found in Foursquare data")
        return
    
    # Load existing results if any
    results = []
    results_file = os.path.join(RESULTS_DIR, 'google_places_results.json')
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
                # Handle both old and new format
                if isinstance(data, dict) and 'restaurants' in data:
                    results = data['restaurants']
                else:
                    results = data
                print(f"Loaded {len(results)} existing results")
        except json.JSONDecodeError:
            print("Error loading existing results, starting fresh")
    
    # Create output directory if it doesn't exist
    ensure_results_dir()
    
    # Process each restaurant
    total = len(restaurants)
    for i, restaurant in enumerate(restaurants, 1):
        name = restaurant['name']
        address = restaurant['address']
        print(f"\nProcessing {i}/{total}: {name} at {address}")
        
        # Skip if we already have results for this restaurant
        if any(r.get('name') == name and r.get('address') == address for r in results):
            print(f"Already have results for {name}, skipping...")
            continue
        
        # Search for the place
        place_data = search_place(name, address)
        if place_data and 'places' in place_data and place_data['places']:
            # Transform the data to match our schema
            transformed_data = transform_to_schema(place_data)
            results.append(transformed_data)
            print(f"Found match for: {name}")
            
            # Save results periodically
            if i % 10 == 0:
                save_results(results)
                print(f"\nSaved {len(results)} results")
        else:
            print(f"No results found for {name}")
        
        # Respect API rate limits
        time.sleep(0.1)
    
    # Save final results
    save_results(results)
    print(f"\nFinished! Saved {len(results)} results to {results_file}")

if __name__ == '__main__':
    main()
