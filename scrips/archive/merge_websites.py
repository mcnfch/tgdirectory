#!/usr/bin/env python3
import json
import os

# Constants
RESULTS_DIR = '/opt/noogabites/Results'
WEBSITES_FILE = os.path.join(RESULTS_DIR, 'Websites.json')
MERGED_FILE = os.path.join(RESULTS_DIR, 'merged', 'merged_restaurant_data_20250212_025740.json')
BACKUP_FILE = MERGED_FILE + '.bak'

def load_json_file(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
        return None

def save_json_file(filepath, data):
    """Save JSON data to file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {str(e)}")
        return False

def main():
    # Load website data
    websites_data = load_json_file(WEBSITES_FILE)
    if not websites_data:
        return
        
    # Load merged data
    merged_data = load_json_file(MERGED_FILE)
    if not merged_data:
        return
        
    # Create website lookup by ID
    website_lookup = {
        restaurant['id']: restaurant['website']
        for restaurant in websites_data.get('restaurants', [])
        if restaurant.get('website')
    }
    
    websites_updated = 0
    
    # Update merged data with websites
    for restaurant in merged_data.get('restaurants', []):
        if 'google_data' in restaurant and restaurant['google_data']:
            place_id = restaurant['google_data'].get('id')
            if place_id and place_id in website_lookup:
                website = website_lookup[place_id]
                restaurant['website'] = website
                restaurant['google_data']['website'] = website
                websites_updated += 1
    
    # First save backup
    if save_json_file(BACKUP_FILE, merged_data):
        print(f"Backup saved to {BACKUP_FILE}")
        
        # Then update original file
        if save_json_file(MERGED_FILE, merged_data):
            print(f"\nProcessing complete!")
            print(f"Websites updated: {websites_updated}")
        else:
            print("\nError saving merged data. Backup is available.")
    else:
        print("\nError creating backup. No changes made.")

if __name__ == '__main__':
    main()
