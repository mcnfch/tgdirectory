#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path

def compare_ids():
    # Define paths
    data_file = Path('/opt/noogabites/public/data/data_20250211_233625.json')
    images_file = Path('/opt/noogabites/Reconcile/folderimages.json')
    output_file = Path('/opt/noogabites/Reconcile/id_differences.json')

    # Read data file
    try:
        with open(data_file) as f:
            data = json.load(f)
            data_ids = {restaurant['google_data']['id'] for restaurant in data['restaurants']}
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    # Read images file
    try:
        with open(images_file) as f:
            images_data = json.load(f)
            image_ids = set(images_data['place_ids'])
    except Exception as e:
        print(f"Error reading images file: {e}")
        return

    # Calculate differences
    missing_from_images = sorted(list(data_ids - image_ids))
    missing_from_data = sorted(list(image_ids - data_ids))

    # Create differential report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_in_data": len(data_ids),
            "total_in_images": len(image_ids),
            "missing_from_images_count": len(missing_from_images),
            "missing_from_data_count": len(missing_from_data)
        },
        "missing_from_images": missing_from_images,
        "missing_from_data": missing_from_data,
        "details": {
            "data_file": str(data_file),
            "images_file": str(images_file)
        }
    }

    # Write report
    try:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Successfully wrote differential report to {output_file}")
        print(f"\nSummary:")
        print(f"Total IDs in data: {len(data_ids)}")
        print(f"Total IDs in images: {len(image_ids)}")
        print(f"Missing from images: {len(missing_from_images)}")
        print(f"Missing from data: {len(missing_from_data)}")
    except Exception as e:
        print(f"Error writing report: {e}")

if __name__ == "__main__":
    compare_ids()
