import json
import requests
import time
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
BASE_URL = "https://places.googleapis.com/v1/places/"
FIELDS = [
    "id",
    "displayName",
    "formattedAddress",
    "primaryType",
    "types",
    "regularOpeningHours",
    "goodForGroups",
    "goodForWatchingSports",
    "liveMusic",
    "outdoorSeating",
    "servesBeer",
    "servesCocktails",
    "servesWine",
    "servesDinner",
    "servesLunch",
    "servesBreakfast",
    "takeout",
    "delivery",
    "reservable"
]

def load_live_data():
    """Load the existing live data file"""
    with open('src/data/static/live_data.json', 'r') as f:
        return json.load(f)

def fetch_place_details(place_id):
    """Fetch extended details for a single place"""
    url = f"{BASE_URL}{place_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }
    params = {
        "fields": ",".join(FIELDS)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for place_id {place_id}: {str(e)}")
        return None

def main():
    # Load existing data
    live_data = load_live_data()
    
    # Get all place IDs
    place_ids = list(live_data['restaurants'].keys())
    total_places = len(place_ids)
    
    # Create new data structure
    extended_data = {
        "metadata": {
            "total_restaurants": total_places,
            "processed_count": 0,
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "processing_status": "completed"
        },
        "restaurants": {}
    }
    
    # Fetch extended data for each place
    for index, place_id in enumerate(place_ids, 1):
        print(f"Fetching data for {place_id} ({index}/{total_places})")
        place_details = fetch_place_details(place_id)
        
        if place_details:
            extended_data['restaurants'][place_id] = place_details
            extended_data['metadata']['processed_count'] += 1
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
        
        # Save progress every 10 places
        if index % 10 == 0:
            with open('src/data/static/extended_live.json', 'w') as f:
                json.dump(extended_data, f, indent=2)
            print(f"Progress saved: {index}/{total_places} places processed")
    
    # Final save
    with open('src/data/static/extended_live.json', 'w') as f:
        json.dump(extended_data, f, indent=2)
    
    print(f"\nProcessed {extended_data['metadata']['processed_count']} of {total_places} places")
    print(f"Results saved to src/data/static/extended_live.json")

if __name__ == "__main__":
    main()
