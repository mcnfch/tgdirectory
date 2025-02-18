#!/usr/bin/env python3
import json
import os

MERGED_FILE = '/opt/noogabites/Results/merged/merged_restaurant_data_20250212_025740.json'

def main():
    with open(MERGED_FILE, 'r') as f:
        data = json.load(f)
    
    total = len(data.get('restaurants', []))
    print(f"\nTotal restaurants in merged data: {total}")

if __name__ == '__main__':
    main()
