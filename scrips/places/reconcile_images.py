#!/usr/bin/env python3

import os
import json
from datetime import datetime
from pathlib import Path

def scan_image_folders():
    # Define paths
    images_dir = Path('/opt/noogabites/public/images')
    output_file = Path('/opt/noogabites/Reconcile/folderimages.json')

    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Get all folder names (Google Place IDs)
    place_ids = []
    try:
        for item in images_dir.iterdir():
            if item.is_dir():
                place_ids.append(item.name)
    except Exception as e:
        print(f"Error scanning image folders: {e}")
        return

    # Create output data structure
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "total_folders": len(place_ids),
        "place_ids": sorted(place_ids)  # Sort for consistency
    }

    # Write to JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Successfully wrote {len(place_ids)} place IDs to {output_file}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    scan_image_folders()
