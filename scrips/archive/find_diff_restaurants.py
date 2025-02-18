#!/usr/bin/env python3
import json
import os
from datetime import datetime

# File paths
RESULTS_DIR = '/opt/noogabites/Results'
FOURSQUARE_FILE = os.path.join(RESULTS_DIR, 'restaurant_results.json')
MERGED_FILE = os.path.join(RESULTS_DIR, 'merged', 'merged_restaurant_data_20250212_025740.json')
DIFF_FILE = os.path.join(RESULTS_DIR, 'restaurant_differential.json')

def load_json_file(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
        return None

def get_restaurant_keys(data, is_foursquare=False):
    """Extract set of restaurant name+address combinations"""
    restaurants = {}
    
    if is_foursquare:
        # Handle Foursquare data structure (organized by cities)
        for city in data.get('cities', []):
            for restaurant in city.get('restaurants', []):
                name = restaurant.get('name', '').strip()
                addr = restaurant.get('address', '').strip()
                key = f"{name}|{addr}".lower()
                restaurants[key] = {
                    "name": name,
                    "address": addr
                }
    else:
        # Handle merged data structure (flat list)
        for restaurant in data.get('restaurants', []):
            name = restaurant.get('name', '').strip()
            addr = restaurant.get('address', '').strip()
            key = f"{name}|{addr}".lower()
            restaurants[key] = {
                "name": name,
                "address": addr
            }
    
    return restaurants

def main():
    # Load data files
    foursquare_data = load_json_file(FOURSQUARE_FILE)
    merged_data = load_json_file(MERGED_FILE)
    
    if not foursquare_data or not merged_data:
        return
    
    # Get restaurant dictionaries
    foursquare_restaurants = get_restaurant_keys(foursquare_data, is_foursquare=True)
    merged_restaurants = get_restaurant_keys(merged_data)
    
    # Find keys unique to foursquare
    unique_keys = set(foursquare_restaurants.keys()) - set(merged_restaurants.keys())
    
    # Create differential data with only unique restaurants
    diff_data = {
        "timestamp": datetime.now().isoformat(),
        "total_unique": len(unique_keys),
        "restaurants": [
            foursquare_restaurants[key]
            for key in sorted(unique_keys)
        ]
    }
    
    # Save differential
    try:
        with open(DIFF_FILE, 'w') as f:
            json.dump(diff_data, f, indent=2)
        print(f"\nDifferential saved to {DIFF_FILE}")
        print(f"Found {len(unique_keys)} unique restaurants")
        
        # Print first few unique restaurants as example
        if unique_keys:
            print("\nExample unique restaurants:")
            for key in sorted(unique_keys)[:5]:
                rest = foursquare_restaurants[key]
                print(f"- {rest['name']} @ {rest['address']}")
    except Exception as e:
        print(f"Error saving differential: {str(e)}")

if __name__ == '__main__':
    main()
