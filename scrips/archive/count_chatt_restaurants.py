#!/usr/bin/env python3
import os
import json
import requests
import time
from dotenv import load_dotenv
from datetime import datetime

# City coordinates and their details
CITIES = {
    "Chattanooga": {"state": "TN", "lat": 35.0456, "lon": -85.3097, "city": "Chattanooga"},
    "Cleveland": {"state": "TN", "lat": 35.1595, "lon": -84.8766, "city": "Cleveland"},
    "Athens": {"state": "TN", "lat": 35.4428, "lon": -84.5929, "city": "Athens"},
    "Soddy-Daisy": {"state": "TN", "lat": 35.2370, "lon": -85.1902, "city": "Soddy-Daisy"},
    "Dalton": {"state": "GA", "lat": 34.7698, "lon": -84.9702, "city": "Dalton"},
    "Calhoun": {"state": "GA", "lat": 34.5023, "lon": -84.9516, "city": "Calhoun"},
    "Rome": {"state": "GA", "lat": 34.2571, "lon": -85.1647, "city": "Rome"}
}

def get_city_restaurants(base_url, headers, city_info):
    """Get restaurants for a city using Places API (New) text search."""
    all_restaurants = []
    seen_places = set()  # Track unique places by their id
    
    # Create the text search query
    query = f"restaurants in {city_info['city']}, {city_info['state']}"
    
    # Add useful fields to get back from the API (advanced tier)
    headers["X-Goog-FieldMask"] = (
        "places.id,"  # For deduplication
        "places.displayName,"  # Restaurant name
        "places.formattedAddress,"  # Full address
        "places.internationalPhoneNumber,"  # Phone number
        "places.websiteUri,"  # Website URL
        "places.rating,"  # Rating out of 5
        "places.userRatingCount,"  # Number of reviews
        "places.googleMapsUri,"  # Link to Google Maps
        "places.primaryTypeDisplayName,"  # Primary business type
        "places.location"  # Lat/lng coordinates
    )
    
    data = {
        "textQuery": query,  # Free text query
        "maxResultCount": 20  # Will get up to 20 results per request
    }
    
    try:
        # Make up to 3 requests to get up to 60 results total
        for page in range(3):  # 20 results per page, up to 3 pages = 60 results
            print(f"\nRequest details for {city_info['city']} (Page {page + 1}):")
            print(f"Query: {query}")
            print(f"URL: {base_url}")
            print("Headers:", json.dumps(headers, indent=2))
            print("Data:", json.dumps(data, indent=2))
            
            # Make the API request
            response = requests.post(base_url, headers=headers, json=data)
            
            # Print response details
            print("\nResponse details:")
            print(f"Status code: {response.status_code}")
            print("Response headers:", json.dumps(dict(response.headers), indent=2))
            print("Response body:", json.dumps(response.json() if response.text else {}, indent=2))
            
            response.raise_for_status()
            result = response.json()
            
            # Add new restaurants from the response
            restaurants = result.get('places', [])
            for restaurant in restaurants:
                place_id = restaurant.get('id')
                if place_id and place_id not in seen_places:
                    seen_places.add(place_id)
                    all_restaurants.append(restaurant)
            
            print(f"Found {len(restaurants)} new restaurants in {city_info['city']} (Page {page + 1})")
            print(f"Total unique restaurants so far: {len(all_restaurants)}")
            
            # If we got less than maxResultCount results, no more pages available
            if len(restaurants) < 20:
                break
                
            # Add a small delay between requests
            time.sleep(2)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching restaurants for {city_info['city']}: {str(e)}")
        raise
        
    return all_restaurants

def get_restaurants_count():
    # Load environment variables
    load_dotenv()
    api_key = os.environ['GOOGLE_PLACES_API_KEY']
    
    if not api_key:
        raise ValueError("GOOGLE_PLACES_API_KEY not found in environment variables")
    
    # Base URL for Places API (New) Text Search
    base_url = "https://places.googleapis.com/v1/places:searchText"
    
    # Headers required for Places API (New)
    headers = {
        'X-Goog-Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Dictionary to store results
    results = {}
    
    # Get current timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Process each city
        for city_name, city_info in CITIES.items():
            print(f"\nProcessing {city_name}, {city_info['state']}...")
            
            # Get restaurants for the city
            restaurants = get_city_restaurants(base_url, headers, city_info)
            
            # Store results
            results[city_name] = {
                'count': len(restaurants),
                'state': city_info['state'],
                'restaurants': restaurants
            }
            
            # Add a small delay between cities to avoid rate limiting
            time.sleep(2)
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Save results to a JSON file
        output_file = f'output/restaurants_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to {output_file}")
        
        # Print summary
        print("\nSummary of restaurants found:")
        print("-" * 50)
        total_restaurants = 0
        for city_name, city_data in results.items():
            count = city_data['count']
            total_restaurants += count
            print(f"{city_name}, {city_data['state']}: {count} restaurants")
        print("-" * 50)
        print(f"Total unique restaurants found: {total_restaurants}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    get_restaurants_count()
