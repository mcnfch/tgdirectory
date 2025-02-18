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
RESULTS_DIR = '/opt/noogabites/Results'
SOURCE_FILE = os.path.join(RESULTS_DIR, 'merged', 'merged_restaurant_data_20250212_025740.json')
OUTPUT_FILE = os.path.join(RESULTS_DIR, 'Websites.json')

# Fields we want to collect
FIELD_MASK = 'places.id,places.displayName,places.websiteUri'

def search_place(restaurant_name, location):
    """Search for a place using restaurant name and location"""
    headers = {
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': FIELD_MASK,
        'Content-Type': 'application/json'
    }
    
    data = {
        'textQuery': f"{restaurant_name} {location}",
        'locationBias': {
            'circle': {
                'center': {
                    'latitude': 35.0456,
                    'longitude': -85.3097
                },
                'radius': 5000.0
            }
        }
    }
    
    try:
        response = requests.post(PLACES_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching for place {restaurant_name}: {str(e)}")
        return None

def load_source_data():
    """Load restaurant data from source file"""
    try:
        with open(SOURCE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading source file: {str(e)}")
        return None

def save_results(results):
    """Save results to output file"""
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def main():
    # Load source data
    source_data = load_source_data()
    if not source_data:
        return
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_restaurants": 0,
        "websites_found": 0,
        "restaurants": []
    }
    
    # Process each restaurant
    for restaurant in source_data.get('restaurants', []):
        name = restaurant.get('name', '')
        city = restaurant.get('city', '')
        state = restaurant.get('state', '')
        location = f"{city}, {state}"
        
        # Search for place
        place_data = search_place(name, location)
        
        if place_data and 'places' in place_data and place_data['places']:
            place = place_data['places'][0]  # Get first match
            website = place.get('websiteUri', '')
            
            results['restaurants'].append({
                "id": place.get('id', ''),
                "name": name,
                "website": website
            })
            
            if website:
                results['websites_found'] += 1
                
            results['total_restaurants'] += 1
            
            # Progress update every 10 restaurants
            if results['total_restaurants'] % 10 == 0:
                print(f"Processed {results['total_restaurants']} restaurants...")
                print(f"Websites found: {results['websites_found']}")
        
        # Respect API rate limits
        time.sleep(0.1)  # Max 10 requests per second
    
    # Save final results
    save_results(results)
    print(f"\nProcessing complete!")
    print(f"Total restaurants processed: {results['total_restaurants']}")
    print(f"Websites found: {results['websites_found']}")

if __name__ == '__main__':
    main()
