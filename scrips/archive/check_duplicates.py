#!/usr/bin/env python3

import json
import os
from difflib import SequenceMatcher
from collections import defaultdict

def load_json_file(file_path):
    """Load JSON data from a file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def normalize_string(s):
    """Normalize string for comparison"""
    return ' '.join(s.lower().split())

def similarity_ratio(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, normalize_string(a), normalize_string(b)).ratio()

def find_duplicates(restaurants, name_threshold=0.85, address_threshold=0.85):
    """Find potential duplicate restaurants based on name and address similarity"""
    potential_duplicates = []
    processed = set()

    # First, group by first letter of name to reduce comparisons
    name_groups = defaultdict(list)
    for i, restaurant in enumerate(restaurants):
        if restaurant['name']:
            first_letter = normalize_string(restaurant['name'])[0]
            name_groups[first_letter].append((i, restaurant))

    # Compare restaurants within each group
    for group in name_groups.values():
        for i, (idx1, rest1) in enumerate(group):
            if idx1 in processed:
                continue

            duplicates = []
            for idx2, rest2 in group[i+1:]:
                if idx2 in processed:
                    continue

                name_similarity = similarity_ratio(rest1['name'], rest2['name'])
                if name_similarity >= name_threshold:
                    # Only check address if names are similar
                    address_similarity = similarity_ratio(rest1['address'], rest2['address'])
                    if address_similarity >= address_threshold:
                        duplicates.append({
                            'index': idx2,
                            'restaurant': rest2,
                            'name_similarity': name_similarity,
                            'address_similarity': address_similarity
                        })

            if duplicates:
                group_info = {
                    'original': {
                        'index': idx1,
                        'restaurant': rest1
                    },
                    'duplicates': duplicates
                }
                potential_duplicates.append(group_info)
                processed.add(idx1)
                processed.update(d['index'] for d in duplicates)

    return potential_duplicates

def print_duplicate_groups(duplicate_groups):
    """Print duplicate groups in a readable format"""
    print(f"\nFound {len(duplicate_groups)} groups of potential duplicates:\n")
    
    for i, group in enumerate(duplicate_groups, 1):
        original = group['original']['restaurant']
        print(f"Group {i}:")
        print(f"Original ({group['original']['index']}):")
        print(f"  Name: {original['name']}")
        print(f"  Address: {original['address']}")
        print(f"  Categories: {', '.join(original.get('categories', []))}")
        print("\nPotential duplicates:")
        
        for dup in group['duplicates']:
            rest = dup['restaurant']
            print(f"  ({dup['index']}):")
            print(f"    Name: {rest['name']} (similarity: {dup['name_similarity']:.2f})")
            print(f"    Address: {rest['address']} (similarity: {dup['address_similarity']:.2f})")
            print(f"    Categories: {', '.join(rest.get('categories', []))}")
        print("\n" + "-"*80 + "\n")

def main():
    # Load the merged data
    merged_file = '/opt/noogabites/Results/merged/merged_restaurant_data_20250212_082235.json'
    print(f"Loading merged data from {merged_file}...")
    data = load_json_file(merged_file)
    restaurants = data['restaurants']
    print(f"Loaded {len(restaurants)} restaurants")

    # Find potential duplicates
    print("\nSearching for potential duplicates...")
    duplicate_groups = find_duplicates(restaurants)
    
    # Print results
    print_duplicate_groups(duplicate_groups)
    
    # Save duplicate groups to a file for reference
    output_file = '/opt/noogabites/Results/merged/duplicate_groups.json'
    with open(output_file, 'w') as f:
        json.dump(duplicate_groups, f, indent=2)
    print(f"\nDuplicate groups saved to: {output_file}")

if __name__ == '__main__':
    main()
