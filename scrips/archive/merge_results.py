#!/usr/bin/env python3

import json
import os
from datetime import datetime

def load_json_file(file_path):
    """Load JSON data from a file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def normalize_name(name):
    """Normalize restaurant name for comparison"""
    return name.lower().strip()

def normalize_address(address):
    """Normalize address for comparison"""
    return address.lower().strip()

def merge_restaurants(existing_data, google_data):
    """Merge restaurant data from both sources"""
    # Create a lookup of existing restaurants by name and address
    restaurant_lookup = {}
    for restaurant in existing_data['restaurants']:
        key = (normalize_name(restaurant['name']), normalize_address(restaurant['address']))
        restaurant_lookup[key] = restaurant

    # Process Google Places results
    for google_restaurant in google_data['restaurants']:
        key = (normalize_name(google_restaurant['name']), normalize_address(google_restaurant['address']))
        
        if key in restaurant_lookup:
            # Update existing restaurant with Google data
            existing = restaurant_lookup[key]
            # Update photos if they exist in Google data
            if google_restaurant.get('photos'):
                existing['photos'] = google_restaurant['photos']
            # Update Google-specific fields
            existing['google_place_id'] = google_restaurant.get('google_place_id', '')
            # Update rating and review count if Google's data is more recent
            if google_restaurant.get('rating'):
                existing['rating'] = google_restaurant['rating']
            if google_restaurant.get('review_count'):
                existing['review_count'] = google_restaurant['review_count']
            # Update website if not present
            if not existing.get('website') and google_restaurant.get('website'):
                existing['website'] = google_restaurant['website']
            # Update phone if not present
            if not existing.get('phone') and google_restaurant.get('phone'):
                existing['phone'] = google_restaurant['phone']
            # Add any new categories
            existing_categories = set(existing.get('categories', []))
            google_categories = set(google_restaurant.get('categories', []))
            existing['categories'] = list(existing_categories | google_categories)
        else:
            # Add new restaurant from Google data
            restaurant_lookup[key] = google_restaurant

    # Create timestamp for the merged file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create the merged data structure
    merged_data = {
        'restaurants': list(restaurant_lookup.values())
    }
    
    return merged_data, timestamp

def main():
    # Define file paths
    base_dir = '/opt/noogabites/Results'
    merged_file = os.path.join(base_dir, 'merged', 'merged_restaurant_data_20250212_025740.json')
    google_file = os.path.join(base_dir, 'google_places_results.json')
    
    # Load both files
    print("Loading existing merged data...")
    existing_data = load_json_file(merged_file)
    print(f"Loaded {len(existing_data['restaurants'])} existing restaurants")
    
    print("\nLoading Google Places data...")
    google_data = load_json_file(google_file)
    print(f"Loaded {len(google_data['restaurants'])} restaurants from Google Places")
    
    # Merge the data
    print("\nMerging data...")
    merged_data, timestamp = merge_restaurants(existing_data, google_data)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(base_dir, 'merged')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save merged results
    output_file = os.path.join(output_dir, f'merged_restaurant_data_{timestamp}.json')
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    print(f"\nMerged data saved to: {output_file}")
    print(f"Total restaurants in merged data: {len(merged_data['restaurants'])}")

if __name__ == '__main__':
    main()
