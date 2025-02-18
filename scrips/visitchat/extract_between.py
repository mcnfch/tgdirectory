import json
import sys

def print_all_restaurants(input_file):
    with open(input_file, 'r') as f:
        restaurants = json.load(f)
    
    print("\nAll restaurants:")
    for r in restaurants:
        if isinstance(r, dict):
            print(f"- {r.get('title')} (Quality Score: {r.get('qualityScore', 'N/A')})")

def extract_between(input_file, start_name, end_name):
    with open(input_file, 'r') as f:
        restaurants = json.load(f)
    
    # Find start and end indices
    start_idx = None
    end_idx = None
    for i, r in enumerate(restaurants):
        if isinstance(r, dict) and r.get('title') == start_name:
            start_idx = i
        elif isinstance(r, dict) and r.get('title') == end_name:
            end_idx = i
    
    if start_idx is None:
        print(f"Could not find start restaurant: {start_name}")
        print("\nAvailable restaurants:")
        for r in restaurants:
            if isinstance(r, dict):
                print(f"- {r.get('title')}")
        return
    if end_idx is None:
        print(f"Could not find end restaurant: {end_name}")
        print("\nAvailable restaurants:")
        for r in restaurants:
            if isinstance(r, dict):
                print(f"- {r.get('title')}")
        return
    
    # Ensure proper order
    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx
    
    # Extract restaurants between (inclusive)
    selected = restaurants[start_idx:end_idx + 1]
    
    # Save to new file
    output_file = '/opt/noogabites/Results/visitchat/restaurants_between.json'
    with open(output_file, 'w') as f:
        json.dump(selected, f, indent=2)
    
    print(f"\nRestaurants between {start_name} and {end_name}:")
    for r in selected:
        if isinstance(r, dict):
            print(f"- {r.get('title')} (Quality Score: {r.get('qualityScore', 'N/A')})")
    print(f"\nSaved {len(selected)} restaurants to {output_file}")

if __name__ == '__main__':
    latest_file = '/opt/noogabites/Results/visitchat/restaurants_20250212_184905.json'
    
    # First print all restaurants
    print_all_restaurants(latest_file)
    
    # Then try to extract between the two restaurants
    start_name = "Clumpies Ice Cream Co./Southside"  
    end_name = "Totto Sushi & Grill"
    
    extract_between(latest_file, start_name, end_name)
