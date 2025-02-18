#!/usr/bin/env python3
import json
import os

MERGED_FILE = '/opt/noogabites/Results/merged/merged_restaurant_data_20250212_025740.json'

def main():
    # Load merged data
    with open(MERGED_FILE, 'r') as f:
        data = json.load(f)
    
    # Get all unique categories
    categories = set()
    for restaurant in data.get('restaurants', []):
        for category in restaurant.get('categories', []):
            categories.add(category)
    
    # Print sorted categories
    print("\nUnique Categories:")
    print("=================")
    for category in sorted(categories):
        print(category)
    print(f"\nTotal unique categories: {len(categories)}")

if __name__ == '__main__':
    main()
