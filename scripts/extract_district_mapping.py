#!/usr/bin/env python3
import json

def extract_district_mapping():
    # Load the live data
    with open('src/data/static/live_data.json', 'r') as f:
        live_data = json.load(f)
    
    # Create district mapping
    district_mapping = {}
    
    # Process each restaurant
    for place_id, data in live_data['restaurants'].items():
        if 'basic_info' in data and 'district' in data['basic_info']:
            district = data['basic_info']['district']
            if district:  # Only include if district exists
                district_mapping[place_id] = district
    
    # Save mapping
    with open('src/data/static/live_districts.json', 'w') as f:
        json.dump(district_mapping, f, indent=2)
    
    # Print summary
    print(f"Total mappings extracted: {len(district_mapping)}")

if __name__ == "__main__":
    extract_district_mapping()
