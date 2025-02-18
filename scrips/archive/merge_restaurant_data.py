#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
from glob import glob

def load_foursquare_data():
    """Load restaurant data from Foursquare results"""
    with open('/opt/noogabites/Results/restaurant_results.json', 'r') as f:
        data = json.load(f)
        restaurants = []
        for city in data['cities']:
            for restaurant in city['restaurants']:
                # Add city and state to restaurant data
                restaurant['city'] = city['city']
                restaurant['state'] = city['state']
                restaurants.append(restaurant)
        return restaurants

def load_google_places_data():
    """Load and deduplicate Google Places data from all progress files"""
    progress_files = glob('/opt/noogabites/Results/places_api_progress_*.json')
    unique_places = {}
    
    for file in progress_files:
        with open(file, 'r') as f:
            places = json.load(f)
            for place in places:
                google_data = place.get('google_data', {})
                place_id = google_data.get('id')
                if place_id:
                    # Keep the most complete record if we have duplicates
                    if place_id not in unique_places or \
                       len(google_data.get('photos', [])) > len(unique_places[place_id].get('google_data', {}).get('photos', [])):
                        unique_places[place_id] = place
    
    return unique_places

def normalize_name(name):
    """Normalize restaurant name for better matching"""
    if not name:
        return ""
    # Remove common suffixes and special characters
    name = name.lower()
    name = name.replace("'", "").replace('"', "").replace("-", " ").replace("&", "and")
    replacements = [
        " restaurant", " grill", " bar", " and ", " kitchen", 
        " steakhouse", " cafe", " diner", " bistro"
    ]
    for r in replacements:
        name = name.replace(r, "")
    return " ".join(name.split())

def merge_restaurant_data(foursquare_data, google_places_data):
    """Merge Foursquare and Google Places data"""
    merged_data = []
    matched_google_ids = set()
    
    # Create a lookup of normalized names to Google place IDs
    name_to_place = {}
    for place_id, place in google_places_data.items():
        name = place.get('foursquare_data', {}).get('name', '')
        if name:
            normalized_name = normalize_name(name)
            if normalized_name:
                name_to_place[normalized_name] = place_id

    # Process each Foursquare restaurant
    for fs_restaurant in foursquare_data:
        restaurant_entry = {
            'name': fs_restaurant['name'],
            'categories': fs_restaurant.get('categories', []),
            'address': fs_restaurant.get('address', ''),
            'city': fs_restaurant.get('city', ''),
            'state': fs_restaurant.get('state', ''),
            'latitude': fs_restaurant.get('latitude'),
            'longitude': fs_restaurant.get('longitude'),
            'phone': fs_restaurant.get('phone', ''),
            'website': fs_restaurant.get('website', ''),
            'hours': fs_restaurant.get('hours', {}),
            'rating': fs_restaurant.get('rating'),
            'price_level': fs_restaurant.get('price_level'),
            'google_data': None
        }
        
        # Try to find matching Google Places data
        normalized_name = normalize_name(fs_restaurant['name'])
        if normalized_name in name_to_place:
            place_id = name_to_place[normalized_name]
            if place_id in google_places_data:
                restaurant_entry['google_data'] = google_places_data[place_id].get('google_data', {})
                matched_google_ids.add(place_id)
        
        merged_data.append(restaurant_entry)
    
    # Add any Google Places entries that weren't matched
    for place_id, place in google_places_data.items():
        if place_id not in matched_google_ids:
            google_data = place.get('google_data', {})
            fs_data = place.get('foursquare_data', {})
            
            restaurant_entry = {
                'name': fs_data.get('name', 'Unknown'),
                'categories': [],  # No categories from Google data
                'address': fs_data.get('address', ''),
                'city': fs_data.get('city', ''),
                'state': fs_data.get('state', ''),
                'latitude': fs_data.get('latitude'),
                'longitude': fs_data.get('longitude'),
                'phone': '',  # These fields would come from Foursquare
                'website': '',
                'hours': {},
                'rating': None,
                'price_level': None,
                'google_data': google_data
            }
            merged_data.append(restaurant_entry)
    
    return merged_data

def main():
    # Load data from both sources
    print("Loading Foursquare data...")
    foursquare_data = load_foursquare_data()
    print(f"Loaded {len(foursquare_data)} restaurants from Foursquare")
    
    print("\nLoading Google Places data...")
    google_places_data = load_google_places_data()
    print(f"Loaded {len(google_places_data)} unique places from Google")
    
    # Merge the data
    print("\nMerging data...")
    merged_data = merge_restaurant_data(foursquare_data, google_places_data)
    print(f"Created {len(merged_data)} merged restaurant entries")
    
    # Save the merged data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'/opt/noogabites/Results/merged_restaurant_data_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump({
            'restaurants': merged_data,
            'metadata': {
                'created_at': timestamp,
                'foursquare_count': len(foursquare_data),
                'google_places_count': len(google_places_data),
                'total_merged': len(merged_data)
            }
        }, f, indent=2)
    
    print(f"\nSaved merged data to: {output_file}")

if __name__ == "__main__":
    main()
