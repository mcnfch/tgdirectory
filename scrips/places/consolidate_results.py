#!/usr/bin/env python3

import os
import json
from datetime import datetime
import glob

def consolidate_results():
    """Consolidate all individual place results into a single file"""
    results_dir = '/opt/noogabites/Results/places'
    output_dir = '/opt/noogabites/Results/places'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all JSON files in results directory
    json_files = glob.glob(os.path.join(results_dir, '*.json'))
    
    if not json_files:
        print("No JSON files found in results directory")
        return
    
    print(f"Found {len(json_files)} JSON files to consolidate")
    
    # Dictionary to store all place data
    consolidated_data = {
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_places": len(json_files)
        },
        "places": []
    }
    
    # Process each JSON file
    for json_file in sorted(json_files):
        try:
            with open(json_file, 'r') as f:
                place_data = json.load(f)
                
            # Add source file info to the place data
            place_data['_source_file'] = os.path.basename(json_file)
            consolidated_data['places'].append(place_data)
            
            # Print progress
            display_name = place_data.get('google_data', {}).get('displayName', 'Unknown')
            print(f"Processed: {display_name}")
            
        except json.JSONDecodeError as e:
            print(f"Error reading {json_file}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error processing {json_file}: {str(e)}")
    
    # Generate output filename with timestamp
    output_file = os.path.join(output_dir, f'consolidated_places_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    # Save consolidated data
    try:
        with open(output_file, 'w') as f:
            json.dump(consolidated_data, f, indent=2)
        print(f"\nSuccessfully consolidated {len(consolidated_data['places'])} places")
        print(f"Output saved to: {output_file}")
    except Exception as e:
        print(f"Error saving consolidated data: {str(e)}")

if __name__ == '__main__':
    consolidate_results()
