import json
import requests
import time
import uuid
from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables
load_dotenv()

# Constants
MAPBOX_TOKEN = os.getenv('NEXT_PUBLIC_MAPBOX')
BASE_URL = "https://api.mapbox.com/search/searchbox/v1"

def load_live_data():
    """Load the existing live data file"""
    with open('src/data/static/live_data.json', 'r') as f:
        return json.load(f)

def get_neighborhood(address):
    """Get neighborhood data for address"""
    # URL encode the address
    encoded_address = quote(address)
    
    # Generate a session token (UUID v4)
    session_token = str(uuid.uuid4())
    
    # First get suggestions
    suggest_url = f"{BASE_URL}/suggest"
    
    params = {
        "q": address,
        "access_token": MAPBOX_TOKEN,
        "session_token": session_token,
        "language": "en",
        "limit": 1,
        "types": "address"
    }
    
    try:
        response = requests.get(suggest_url, params=params)
        response.raise_for_status()
        suggest_data = response.json()
        
        if suggest_data.get("suggestions") and len(suggest_data["suggestions"]) > 0:
            suggestion = suggest_data["suggestions"][0]
            
            # Get the mapbox_id for retrieval
            mapbox_id = suggestion.get("mapbox_id")
            
            if mapbox_id:
                # Now retrieve the full feature details
                retrieve_url = f"{BASE_URL}/retrieve/{mapbox_id}"
                retrieve_params = {
                    "access_token": MAPBOX_TOKEN,
                    "session_token": session_token
                }
                
                retrieve_response = requests.get(retrieve_url, params=retrieve_params)
                retrieve_response.raise_for_status()
                feature_data = retrieve_response.json()
                
                # Extract neighborhood from feature context
                if "features" in feature_data and len(feature_data["features"]) > 0:
                    feature = feature_data["features"][0]
                    context = feature.get("properties", {}).get("context", {})
                    
                    # Look for neighborhood in context
                    neighborhood = context.get("neighborhood", {})
                    if neighborhood:
                        return {
                            "name": neighborhood.get("name"),
                            "id": neighborhood.get("id"),
                            "full_context": context,
                            "feature_type": feature.get("type"),
                            "coordinates": feature.get("geometry", {}).get("coordinates")
                        }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {address}: {str(e)}")
        return None

def main():
    # Load live data
    live_data = load_live_data()
    
    # Create districts data structure
    districts_data = {
        "metadata": {
            "total_restaurants": len(live_data['restaurants']),
            "processed_count": 0,
            "districts_found": 0,
            "restaurants_without_district": 0,
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "districts": {},
        "restaurants": {},
        "unmatched_restaurants": {}
    }
    
    # Process each restaurant
    for restaurant_id, restaurant in live_data['restaurants'].items():
        print(f"Processing {restaurant['basic_info']['name']}")
        
        # Get address
        address = restaurant['location']['formatted_address']
        
        # Get neighborhood data
        neighborhood = get_neighborhood(address)
        
        if neighborhood and neighborhood.get("name"):
            district_name = neighborhood["name"]
            
            # Add to districts if not exists
            if district_name not in districts_data["districts"]:
                districts_data["districts"][district_name] = {
                    "name": district_name,
                    "id": neighborhood["id"],
                    "context": neighborhood["full_context"],
                    "restaurant_count": 0
                }
                districts_data["metadata"]["districts_found"] += 1
            
            # Add restaurant to district count
            districts_data["districts"][district_name]["restaurant_count"] += 1
            
            # Add district info to restaurant
            districts_data["restaurants"][restaurant_id] = {
                "name": restaurant['basic_info']['name'],
                "district": district_name,
                "coordinates": neighborhood["coordinates"]
            }
            
            districts_data["metadata"]["processed_count"] += 1
        else:
            # Track restaurants without district data
            districts_data["unmatched_restaurants"][restaurant_id] = {
                "name": restaurant['basic_info']['name'],
                "address": address
            }
            districts_data["metadata"]["restaurants_without_district"] += 1
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
        
        # Save progress every 10 restaurants
        if districts_data["metadata"]["processed_count"] % 10 == 0:
            with open('src/data/static/live_districts.json', 'w') as f:
                json.dump(districts_data, f, indent=2)
            print(f"Progress saved: {districts_data['metadata']['processed_count']} restaurants processed")
    
    # Final save
    with open('src/data/static/live_districts.json', 'w') as f:
        json.dump(districts_data, f, indent=2)
    
    print(f"\nProcessed {districts_data['metadata']['processed_count']} restaurants")
    print(f"Found {districts_data['metadata']['districts_found']} districts")
    print(f"Restaurants without district: {districts_data['metadata']['restaurants_without_district']}")
    print("Results saved to src/data/static/live_districts.json")

if __name__ == "__main__":
    main()
