#!/usr/bin/env python3
import json
import os
import time
import requests
from datetime import datetime
from env import GOOGLE_PLACES_API_KEY

# Constants
RESULTS_DIR = '/opt/noogabites/Results'
DIFF_FILE = os.path.join(RESULTS_DIR, 'restaurant_differential.json')
OUTPUT_FILE = os.path.join(RESULTS_DIR, 'differential_google_data.json')
SEARCH_URL = 'https://places.googleapis.com/v1/places:searchText'

def load_json_file(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
        return None

def search_place(name, address):
    """Search for a place using restaurant name and address"""
    headers = {
        'X-Goog-Api-Key': GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.id,places.formattedAddress,places.location,places.displayName,places.primaryType,places.types,places.websiteUri,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.priceLevel',
        'Content-Type': 'application/json'
    }
    
    data = {
        'textQuery': f"{name} {address}",
        'locationBias': {
            'circle': {
                'center': {
                    'latitude': 35.0456,
                    'longitude': -85.3097
                },
                'radius': 50000.0
            }
        },
        'languageCode': 'en'
    }
    
    try:
        response = requests.post(SEARCH_URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error searching for place {name}: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        print(f"Timeout searching for place {name}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error searching for place {name}: {str(e)}")
        return None

def main():
    # Load differential data
    diff_data = load_json_file(DIFF_FILE)
    if not diff_data:
        return
    
    results = []
    processed = 0
    found = 0
    
    # Process each restaurant
    try:
        for restaurant in diff_data.get('restaurants', []):
            name = restaurant.get('name', '').strip()
            address = restaurant.get('address', '').strip()
            
            # Search for the place
            search_result = search_place(name, address)
            
            if search_result and 'places' in search_result and search_result['places']:
                place = search_result['places'][0]  # Get first match
                results.append({
                    'name': name,
                    'address': address,
                    'google_data': place
                })
                found += 1
                print(f"Found match for: {name}")
            else:
                print(f"No match for: {name}")
            
            processed += 1
            if processed % 10 == 0:
                print(f"\nProcessed {processed}/{diff_data['total_unique']} restaurants...")
                print(f"Found {found} matches\n")
                
                # Save intermediate results
                output_data = {
                    'timestamp': datetime.now().isoformat(),
                    'total_processed': processed,
                    'total_found': found,
                    'restaurants': results
                }
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(output_data, f, indent=2)
                print("Saved intermediate results")
            
            # Respect API rate limits (20 QPS)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        # Save final results
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'total_processed': processed,
            'total_found': found,
            'restaurants': results
        }
        
        try:
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\nResults saved to {OUTPUT_FILE}")
            print(f"Total restaurants processed: {processed}")
            print(f"Total matches found: {found}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

if __name__ == '__main__':
    main()
