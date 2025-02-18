#!/usr/bin/env python3
import json
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
MAPBOX_TOKEN = os.getenv('NEXT_PUBLIC_MAPBOX')

def get_district_from_mapbox(coordinates):
    """Get district using Mapbox reverse endpoint"""
    base_url = "https://api.mapbox.com/search/searchbox/v1/reverse"
    
    # Convert coordinates to string query
    lon, lat = coordinates
    
    params = {
        'longitude': lon,
        'latitude': lat,
        'access_token': MAPBOX_TOKEN,
        'limit': 1,
        'types': 'neighborhood',
        'language': 'en'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('features') and len(data['features']) > 0:
            return data['features'][0]['properties']['name']
    return None

def update_missing_districts():
    # Load the live data
    with open('src/data/static/live_data.json', 'r') as f:
        live_data = json.load(f)
    
    # Track changes
    updated_count = 0
    missing_count = 0
    total_processed = 0
    
    # Create backup
    with open('src/data/static/live_data.backup.json', 'w') as f:
        json.dump(live_data, f, indent=2)
    
    # Process each restaurant
    for place_id, data in live_data['restaurants'].items():
        if 'basic_info' in data:
            basic_info = data['basic_info']
            
            # Only process if district is missing and coordinates exist
            if ('district' not in basic_info or not basic_info['district']) and 'coordinates' in basic_info:
                print(f"\nProcessing Place ID: {place_id}")
                coordinates = basic_info['coordinates']
                
                district = get_district_from_mapbox(coordinates)
                if district:
                    print(f"Found district: {district}")
                    basic_info['district'] = district
                    updated_count += 1
                else:
                    print(f"No district found for coordinates: {coordinates}")
                    missing_count += 1
                
                # Rate limiting - 1 request per second
                time.sleep(1)
            
            total_processed += 1
    
    # Save updated data
    with open('src/data/static/live_data.json', 'w') as f:
        json.dump(live_data, f, indent=2)
    
    print("\nSummary:")
    print(f"Total restaurants processed: {total_processed}")
    print(f"Districts updated: {updated_count}")
    print(f"Districts still missing: {missing_count}")

if __name__ == "__main__":
    update_missing_districts()
