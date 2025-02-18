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
BACKUP_FILE = SOURCE_FILE + '.bak'

def search_place(restaurant_name, location):
    """Search for a place using restaurant name and location"""
    headers = {
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.id,places.websiteUri',
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

def save_data(data):
    """Save updated data back to source file"""
    try:
        # First create a backup
        with open(BACKUP_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Backup saved to {BACKUP_FILE}")
        
        # Then update the original file
        with open(SOURCE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {SOURCE_FILE}")
        return True
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        return False

def main():
    # Load source data
    data = load_source_data()
    if not data:
        return
    
    websites_updated = 0
    total_processed = 0
    
    # Process each restaurant
    for restaurant in data.get('restaurants', []):
        name = restaurant.get('name', '')
        city = restaurant.get('city', '')
        state = restaurant.get('state', '')
        location = f"{city}, {state}"
        
        # Search for place
        place_data = search_place(name, location)
        
        if place_data and 'places' in place_data and place_data['places']:
            place = place_data['places'][0]  # Get first match
            website = place.get('websiteUri', '')
            
            if website:
                # Update both locations for website data
                restaurant['website'] = website
                if 'google_data' not in restaurant:
                    restaurant['google_data'] = {}
                restaurant['google_data']['website'] = website
                websites_updated += 1
            
        total_processed += 1
        
        # Progress update every 10 restaurants
        if total_processed % 10 == 0:
            print(f"Processed {total_processed} restaurants...")
            print(f"Updated {websites_updated} websites")
        
        # Respect API rate limits
        time.sleep(0.1)  # Max 10 requests per second
    
    # Save the updated data
    if save_data(data):
        print(f"\nProcessing complete!")
        print(f"Total restaurants processed: {total_processed}")
        print(f"Websites updated: {websites_updated}")
    else:
        print("\nError saving data. Check the backup file.")

if __name__ == '__main__':
    main()
