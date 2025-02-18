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

def create_district_mapping():
    # Load the live data
    with open('src/data/static/live_data.json', 'r') as f:
        live_data = json.load(f)
    
    # Create mapping
    district_mapping = {}
    processed_count = 0
    success_count = 0
    
    # Process each restaurant
    for place_id, data in live_data['restaurants'].items():
        if 'basic_info' in data and 'coordinates' in data['basic_info']:
            coordinates = data['basic_info']['coordinates']
            print(f"\nProcessing Place ID: {place_id}")
            print(f"Coordinates: {coordinates}")
            
            district = get_district_from_mapbox(coordinates)
            if district:
                print(f"Found district: {district}")
                district_mapping[place_id] = district
                success_count += 1
            else:
                print(f"No district found")
            
            processed_count += 1
            
            # Rate limiting - 1 request per second
            time.sleep(1)
    
    # Add metadata
    output = {
        "metadata": {
            "total_processed": processed_count,
            "districts_found": success_count,
            "last_updated": "2025-02-18T18:14:41Z"
        },
        "places_to_districts": district_mapping
    }
    
    # Save mapping to new file
    with open('src/data/static/places_districts.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nSummary:")
    print(f"Total places processed: {processed_count}")
    print(f"Districts found: {success_count}")

if __name__ == "__main__":
    create_district_mapping()
