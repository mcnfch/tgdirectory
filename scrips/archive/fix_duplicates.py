#!/usr/bin/env python3

import json
import os
from datetime import datetime

def load_json_file(file_path):
    """Load JSON data from a file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def merge_duplicate_restaurants(data):
    """Merge the identified duplicate restaurants"""
    restaurants = data['restaurants']
    
    # Find Tony's Pasta Shop entries
    tonys_indices = []
    for i, rest in enumerate(restaurants):
        if rest['name'] == "Tony's Pasta Shop & Trattoria":
            tonys_indices.append(i)
    
    if len(tonys_indices) == 2:
        # Keep the first one and merge data from the second
        rest1 = restaurants[tonys_indices[0]]
        rest2 = restaurants[tonys_indices[1]]
        
        # Merge categories
        categories = set(rest1.get('categories', []))
        categories.update(rest2.get('categories', []))
        rest1['categories'] = list(categories)
        
        # Remove the second entry
        restaurants.pop(tonys_indices[1])
        
        print("Merged duplicate entries for Tony's Pasta Shop & Trattoria")
    
    return {'restaurants': restaurants}

def main():
    # Load the merged data
    merged_file = '/opt/noogabites/Results/merged/merged_restaurant_data_20250212_082235.json'
    print(f"Loading merged data from {merged_file}...")
    data = load_json_file(merged_file)
    
    # Merge duplicates
    print("\nMerging duplicate restaurants...")
    cleaned_data = merge_duplicate_restaurants(data)
    
    # Save the cleaned data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'/opt/noogabites/Results/merged/merged_restaurant_data_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"\nCleaned data saved to: {output_file}")
    print(f"Total restaurants: {len(cleaned_data['restaurants'])}")

if __name__ == '__main__':
    main()
