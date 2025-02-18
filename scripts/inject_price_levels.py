#!/usr/bin/env python3

import json
import sys
from datetime import datetime
from pathlib import Path

# Constants
LIVE_DATA_PATH = Path(__file__).parent.parent / "src" / "data" / "static" / "live_data.json"
PRICE_LEVELS_PATH = Path(__file__).parent.parent / "src" / "data" / "static" / "price_levels.json"

def load_json(file_path):
    """Load a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        sys.exit(1)

def save_json(file_path, data):
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        sys.exit(1)

def get_numeric_price_level(price_level_str):
    """Convert price level string to numeric value."""
    price_level_map = {
        "PRICE_LEVEL_FREE": 0,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4
    }
    return price_level_map.get(price_level_str)

def main():
    print("Loading data files...")
    live_data = load_json(LIVE_DATA_PATH)
    price_levels = load_json(PRICE_LEVELS_PATH)

    if price_levels["metadata"]["processing_status"] != "completed":
        print("Warning: Price levels data is not fully processed!")
        response = input("Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborting.")
            sys.exit(0)

    print("\nInjecting price levels into live data...")
    updated_count = 0
    missing_count = 0

    for place_id, restaurant in live_data["restaurants"].items():
        if place_id in price_levels["price_levels"]:
            price_level_str = price_levels["price_levels"][place_id]
            restaurant["basic_info"]["price_level"] = {
                "value": price_level_str,
                "numeric": get_numeric_price_level(price_level_str)
            }
            updated_count += 1
        else:
            missing_count += 1

    # Update metadata
    live_data["metadata"]["price_level_update"] = {
        "last_updated": price_levels["metadata"]["last_updated"],
        "total_with_price": updated_count,
        "total_restaurants": price_levels["metadata"]["total_restaurants"],
        "missing_price_data": missing_count
    }

    print("\nSaving updated live data...")
    save_json(LIVE_DATA_PATH, live_data)

    print("\nUpdate completed successfully!")
    print(f"Total restaurants processed: {updated_count + missing_count}")
    print(f"Restaurants updated with price levels: {updated_count}")
    print(f"Restaurants missing price data: {missing_count}")

if __name__ == "__main__":
    main()
