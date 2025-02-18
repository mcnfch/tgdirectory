#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime
from typing import Dict, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')

# Constants
PLACES_API_URL = 'https://places.googleapis.com/v1/places:searchNearby'
RESULTS_DIR = '/opt/noogabites/Results/google_places'

def load_cities() -> List[Dict]:
    """Load cities from JSON file"""
    with open('/opt/noogabites/public/data/cities.json', 'r') as f:
        return json.load(f)

def get_restaurants_for_city(city_name: str, city_data: Dict, radius_meters: float = 5000) -> Dict:
    """Get restaurant names for a city"""
    print(f"Fetching restaurants for {city_name}...")
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.displayName'
    }
    
    restaurants = []
    page_token = None
    max_pages = 5  # Limit to 100 results (5 pages * 20 results)
    current_page = 0
    
    while current_page < max_pages:
        data = {
            'includedTypes': ['restaurant'],
            'maxResultCount': 20,
            'rankPreference': 'DISTANCE',
            'locationRestriction': {
                'circle': {
                    'center': {
                        'latitude': city_data['location']['latitude'],
                        'longitude': city_data['location']['longitude']
                    },
                    'radius': str(radius_meters)
                }
            }
        }
        
        if page_token:
            data['pageToken'] = page_token
        
        try:
            response = requests.post(PLACES_API_URL, json=data, headers=headers)
            if response.status_code != 200:
                break
                
            results = response.json()
            
            # Process places in this page
            for place in results.get('places', []):
                display_name = place.get('displayName', {})
                name = display_name.get('text', '') if isinstance(display_name, dict) else str(display_name)
                if name:
                    restaurants.append(name)
            
            # Check if there are more pages
            page_token = results.get('nextPageToken')
            if not page_token:
                break
            
            current_page += 1
            time.sleep(1)
            
        except:
            break
    
    print(f"Found {len(restaurants)} restaurants in {city_name}")
    return {
        'city': city_name,
        'state': city_data['state'],
        'restaurants': restaurants
    }

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(RESULTS_DIR, f'restaurant_names_{timestamp}.json')
    
    cities = load_cities()
    results = []
    
    for city_data in cities:
        city_name = city_data['name']
        result = get_restaurants_for_city(city_name, city_data)
        results.append(result)
        
        # Save after each city
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        time.sleep(2)
    
    print(f"\nResults saved to {output_file}")

if __name__ == '__main__':
    main()