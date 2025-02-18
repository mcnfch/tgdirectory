#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Dict, Any, List
import shutil
from datetime import datetime

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load a JSON file and return its contents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding {file_path}: {e}")
        return {}
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file with pretty printing."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def backup_directory(src_dir: str) -> str:
    """Create a backup of the static directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{src_dir}_backup_{timestamp}"
    try:
        shutil.copytree(src_dir, backup_dir)
        print(f"Created backup at: {backup_dir}")
        return backup_dir
    except Exception as e:
        print(f"Error creating backup: {e}")
        return ""

def merge_restaurant_data(live_data: Dict[str, Any], extended_data: Dict[str, Any], district_data: Dict[str, Any]) -> Dict[str, Any]:
    """Merge restaurant data from multiple sources while maintaining the original structure."""
    merged = {
        "metadata": live_data.get("metadata", {}),
        "restaurants": {}
    }
    
    # Create lookup dictionaries for faster access
    extended_lookup = {item.get('id'): item for item in extended_data.get('items', [])}
    
    # Create district lookup from the restaurants section of district_data
    district_lookup = {}
    for rest_id, rest_info in district_data.get('restaurants', {}).items():
        district_name = rest_info.get('district')
        if district_name:
            district_info = district_data['districts'].get(district_name, {})
            district_lookup[rest_id] = {
                'district': district_name,
                'district_description': district_info.get('description', ''),
                'coordinates': rest_info.get('coordinates', [])
            }
    
    # Process each restaurant
    for rest_id, restaurant in live_data.get('restaurants', {}).items():
        # Start with the base restaurant data
        merged_restaurant = restaurant.copy()
        
        # Merge extended data if available
        if rest_id in extended_lookup:
            ext_data = extended_lookup[rest_id]
            for key, value in ext_data.items():
                if key not in merged_restaurant.get('basic_info', {}) and value:
                    if 'basic_info' not in merged_restaurant:
                        merged_restaurant['basic_info'] = {}
                    merged_restaurant['basic_info'][key] = value
        
        # Add district information if available
        if rest_id in district_lookup:
            district_info = district_lookup[rest_id]
            if 'basic_info' not in merged_restaurant:
                merged_restaurant['basic_info'] = {}
            merged_restaurant['basic_info']['district'] = district_info['district']
            merged_restaurant['basic_info']['district_description'] = district_info['district_description']
            if 'coordinates' not in merged_restaurant['basic_info'] and district_info['coordinates']:
                merged_restaurant['basic_info']['coordinates'] = district_info['coordinates']
        
        # Add to merged data
        merged['restaurants'][rest_id] = merged_restaurant
    
    # Update metadata
    merged['metadata'].update({
        'last_updated': datetime.now().isoformat(),
        'data_sources': ['live_data.json', 'extended_live.json', 'live_districts.json'],
        'district_stats': district_data.get('metadata', {})
    })
    
    return merged

def validate_data(data: Dict[str, Any]) -> List[str]:
    """Validate the merged data structure."""
    errors = []
    
    # Check basic structure
    if not isinstance(data.get('restaurants'), dict):
        errors.append("Missing or invalid 'restaurants' object")
        return errors
    
    # Validate each restaurant entry
    required_fields = ['name', 'id']
    for rest_id, restaurant in data.get('restaurants', {}).items():
        if not isinstance(restaurant, dict):
            errors.append(f"Invalid restaurant entry for ID {rest_id}")
            continue
            
        # Check basic_info exists
        if 'basic_info' not in restaurant:
            errors.append(f"Missing 'basic_info' for restaurant {rest_id}")
            continue
            
        # Check required fields in basic_info
        basic_info = restaurant['basic_info']
        for field in required_fields:
            if field not in basic_info:
                errors.append(f"Missing required field '{field}' in basic_info for restaurant {rest_id}")
    
    return errors

def main():
    # Define paths
    static_dir = Path("/opt/tgdirectory/src/data/static")
    output_file = static_dir / "enriched_live_data.json"
    
    # Create backup
    backup_dir = backup_directory(str(static_dir))
    if not backup_dir:
        print("Backup failed, aborting.")
        return

    # Load source files
    live_data = load_json_file(str(static_dir / "live_data.json"))
    extended_data = load_json_file(str(static_dir / "extended_live.json"))
    district_data = load_json_file(str(static_dir / "live_districts.json"))
    
    if not live_data or not extended_data or not district_data:
        print("Error loading source files. Aborting.")
        return
    
    # Merge data
    print("Merging restaurant data...")
    merged_data = merge_restaurant_data(live_data, extended_data, district_data)
    
    # Validate merged data
    print("Validating merged data...")
    validation_errors = validate_data(merged_data)
    if validation_errors:
        print("\nValidation errors found:")
        for error in validation_errors:
            print(f"- {error}")
        print("\nProceeding with save despite validation errors...")
    
    # Save merged data
    save_json_file(merged_data, str(output_file))
    print(f"\nEnriched data saved to: {output_file}")
    
    # Print summary
    print("\nData summary:")
    print(f"Total restaurants: {len(merged_data.get('restaurants', {}))}")
    print(f"Data sources: {', '.join(merged_data.get('metadata', {}).get('data_sources', []))}")
    print(f"Last updated: {merged_data.get('metadata', {}).get('last_updated')}")

if __name__ == "__main__":
    main()
