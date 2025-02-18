#!/usr/bin/env python3

import json
import os
import time
from datetime import datetime, timezone
import requests
from pathlib import Path

# Constants
GOOGLE_PLACES_API_KEY = os.getenv('NEXT_PUBLIC_GOOGLE_PLACES_API_KEY')
BASE_URL = "https://places.googleapis.com/v1/places"
LIVE_DATA_PATH = Path(__file__).parent.parent / "src" / "data" / "static" / "live_data.json"
PRICE_LEVELS_PATH = Path(__file__).parent.parent / "src" / "data" / "static" / "price_levels.json"

def load_live_data():
    """Load the live data JSON file."""
    try:
        with open(LIVE_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading live data: {e}")
        return None

def fetch_price_level(place_id):
    """Fetch price level for a single place ID."""
    url = f"{BASE_URL}/{place_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
    }
    params = {
        "fields": "id,priceLevel"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("priceLevel")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price level for {place_id}: {e}")
        return None

def main():
    # Load existing price levels if available
    existing_price_levels = {}
    if PRICE_LEVELS_PATH.exists():
        try:
            with open(PRICE_LEVELS_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_price_levels = existing_data.get("price_levels", {})
        except Exception as e:
            print(f"Error loading existing price levels: {e}")

    # Load live data
    live_data = load_live_data()
    if not live_data:
        print("Failed to load live data")
        return

    restaurants = live_data.get("restaurants", {})
    total_restaurants = len(restaurants)
    print(f"Found {total_restaurants} restaurants to process")

    # Initialize results dictionary with existing data
    results = {
        "metadata": {
            "total_restaurants": total_restaurants,
            "processed_count": 0,
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "processing_status": "in_progress"
        },
        "price_levels": existing_price_levels.copy()
    }

    # Process each restaurant
    for i, (place_id, _) in enumerate(restaurants.items(), 1):
        # Skip if we already have the price level
        if place_id in existing_price_levels:
            print(f"[{i}/{total_restaurants}] Already have price level for {place_id}")
            results["metadata"]["processed_count"] += 1
            continue

        print(f"[{i}/{total_restaurants}] Processing {place_id}")
        
        price_level = fetch_price_level(place_id)
        if price_level:
            results["price_levels"][place_id] = price_level
            results["metadata"]["processed_count"] += 1

        # Save progress every 10 restaurants
        if i % 10 == 0:
            results["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            with open(PRICE_LEVELS_PATH, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)

        # Respect API rate limits
        time.sleep(0.2)  # 5 requests per second should be safe

    # Final save
    results["metadata"]["processing_status"] = "completed"
    results["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(PRICE_LEVELS_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nProcessing completed!")
    print(f"Total restaurants processed: {results['metadata']['processed_count']}")
    print(f"Results saved to: {PRICE_LEVELS_PATH}")

if __name__ == "__main__":
    main()
