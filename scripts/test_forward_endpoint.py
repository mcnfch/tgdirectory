#!/usr/bin/env python3
import json
import requests
import os
from dotenv import load_dotenv

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
        print(f"Full response for coordinates {lon},{lat}:")
        print(json.dumps(data, indent=2))
        return data
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_forward_endpoint():
    # Load the live data
    with open('src/data/static/live_data.json', 'r') as f:
        live_data = json.load(f)
    
    # Get next 3 entries with coordinates
    count = 0
    results = {}
    
    for place_id, data in live_data['restaurants'].items():
        if count >= 3:
            break
            
        if 'basic_info' in data:
            basic_info = data['basic_info']
            if 'coordinates' in basic_info:
                coordinates = basic_info['coordinates']
                print(f"\nTesting Place ID: {place_id}")
                print(f"Current district: {basic_info.get('district', 'None')}")
                print(f"Coordinates: {coordinates}")
                
                mapbox_data = get_district_from_mapbox(coordinates)
                if mapbox_data:
                    results[place_id] = {
                        'coordinates': coordinates,
                        'current_district': basic_info.get('district'),
                        'mapbox_response': mapbox_data
                    }
                count += 1
    
    # Save results
    with open('src/data/static/forward_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    test_forward_endpoint()
