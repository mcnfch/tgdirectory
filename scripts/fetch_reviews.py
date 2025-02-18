#!/usr/bin/env python3

import json
import time
import requests
from pathlib import Path

API_KEY = "AIzaSyBcAqAEaacjrBQ3oFe9fNzAUm1oe3E_cDQ"
BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"
LIVE_DATA_PATH = Path(__file__).parent.parent / "src/data/static/live_data.json"
OUTPUT_PATH = Path(__file__).parent.parent / "src/data/static/place_reviews.json"

def fetch_place_reviews(place_id):
    """Fetch reviews for a single place ID."""
    params = {
        "place_id": place_id,
        "fields": "reviews",
        "reviews_sort": "newest",
        "key": API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "OK":
            return data["result"].get("reviews", [])
        else:
            print(f"Error fetching reviews for {place_id}: {data['status']}")
            return []
            
    except Exception as e:
        print(f"Exception fetching reviews for {place_id}: {str(e)}")
        return []

def main():
    # Load live data
    with open(LIVE_DATA_PATH, 'r') as f:
        live_data = json.load(f)
    
    # Initialize results dictionary
    results = {}
    total_places = len(live_data["restaurants"])
    
    print(f"Fetching reviews for {total_places} places...")
    
    # Process each place
    for i, (place_id, place_data) in enumerate(live_data["restaurants"].items(), 1):
        print(f"Processing {i}/{total_places}: {place_data['basic_info']['name']}")
        
        reviews = fetch_place_reviews(place_id)
        results[place_id] = {
            "name": place_data["basic_info"]["name"],
            "reviews": reviews
        }
        
        # Sleep to avoid hitting rate limits
        if i < total_places:
            time.sleep(0.5)  # 500ms delay between requests
    
    # Save results
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone! Reviews saved to {OUTPUT_PATH}")
    print(f"Total places processed: {len(results)}")

if __name__ == "__main__":
    main()
