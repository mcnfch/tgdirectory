#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
PLACES_API_BASE = "https://places.googleapis.com/v1/places"

class GooglePlacesFetcher:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = PLACES_API_BASE

    def search_place(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for a place using the Places API v1 Text Search
        """
        endpoint = f"{self.base_url}:searchText"
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location'
        }
        
        data = {
            "textQuery": query,
            "languageCode": "en"
        }
        
        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if data.get("places"):
                return data["places"][0]
        return None

    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place using Places API v1
        """
        endpoint = f"{self.base_url}/{place_id}"
        headers = {
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'id,displayName,formattedAddress,location,rating,userRatingCount,'
                               'websiteUri,regularOpeningHours,priceLevel,photos,types,delivery,'
                               'dineIn,takeout,reservable,servesBeer,servesWine,servesCocktails,'
                               'servesVegetarianFood,servesDinner,servesLunch,servesBreakfast'
        }
        
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def fetch_and_save_photos(self, photo_references: list, output_dir: str) -> list:
        """
        Fetch and save photos using their reference IDs
        Note: Photo handling in Places API v1 is different and needs to be implemented
        """
        # TODO: Implement photo fetching for Places API v1
        return []

def main():
    # Initialize fetcher
    fetcher = GooglePlacesFetcher()
    
    # Search for St. John's Restaurant
    query = "St John's Restaurant Chattanooga Tennessee"
    search_result = fetcher.search_place(query)
    
    if not search_result:
        print("Restaurant not found!")
        return
    
    # Get detailed information
    place_id = search_result["id"]
    details = fetcher.get_place_details(place_id)
    
    if not details:
        print("Could not fetch restaurant details!")
        return
    
    # Create output directory for results
    output_dir = os.path.join(os.path.dirname(__file__), "st_johns_data")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save all details to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"st_johns_details_{timestamp}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "search_result": search_result,
            "details": details,
            "fetch_time": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Data successfully saved to {output_file}")

if __name__ == "__main__":
    main()
