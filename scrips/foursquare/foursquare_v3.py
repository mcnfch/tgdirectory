#!/usr/bin/env python3
import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load cities from JSON file
with open('/opt/noogabites/public/data/cities.json', 'r') as f:
    cities_list = json.load(f)
    
# Convert to the format expected by the rest of the code
CITIES = {
    city['name']: {
        'state': city['state'],
        'lat': city['location']['latitude'],
        'lon': city['location']['longitude'],
        'city': city['name']
    }
    for city in cities_list
}

class FoursquareAPI:
    """Foursquare Places API v3 client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3"
        self.headers = {
            "Accept": "application/json",
            "Authorization": api_key
        }
    
    def search_places(
        self,
        lat: float,
        lon: float,
        radius: int = 10000,  # Increased to 10km
        categories: str = "13065,13067,13068,13070,13071,13072,13073,13074,13075,13076",  # Restaurant categories
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> Dict:
        """
        Search for places using Foursquare Places API
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in meters
            categories: Category IDs (13065 = Restaurants, plus subcategories)
            limit: Number of results per page
            cursor: Pagination cursor
        
        Returns:
            API response as dictionary
        """
        endpoint = f"{self.base_url}/places/search"
        
        params = {
            "ll": f"{lat},{lon}",
            "radius": radius,
            "categories": categories,
            "limit": limit,
            "sort": "DISTANCE",
            "fields": ",".join([
                "fsq_id",
                "name",
                "categories",
                "chains",
                "distance",
                "location",
                "geocodes",
                "website",
                "social_media",
                "menu",
                "rating",
                "stats",
                "popularity",
                "price",
                "hours",
                "tel",
                "email",
                "verified",
                "features",
                "tastes",
                "tips"
            ])
        }
        
        if cursor:
            params["cursor"] = cursor
            
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in API request: {str(e)}")
            if response.status_code == 429:  # Rate limit exceeded
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limit exceeded. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self.search_places(lat, lon, radius, categories, limit, cursor)
            return {"error": str(e)}

def get_restaurants_for_city(api: FoursquareAPI, city_name: str, city_data: Dict) -> Dict:
    """
    Get all restaurants for a specific city
    
    Args:
        api: FoursquareAPI instance
        city_name: Name of the city
        city_data: Dictionary containing city details
    
    Returns:
        Dictionary containing city restaurant data
    """
    print(f"\nFetching restaurants for {city_name}, {city_data['state']}...")
    
    restaurants = []
    cursor = None
    total_results = 0
    
    while True:
        result = api.search_places(
            lat=city_data['lat'],
            lon=city_data['lon'],
            cursor=cursor
        )
        
        if "error" in result:
            print(f"Error fetching data for {city_name}: {result['error']}")
            break
            
        # Add restaurants from this page and print names for debugging
        for place in result.get('results', []):
            restaurants.append(place)
            if 'name' in place:
                print(f"Found restaurant: {place['name']}")
        
        total_results = len(restaurants)
        
        # Get cursor for next page
        cursor = result.get('cursor')
        if not cursor:
            break
            
        print(f"Found {total_results} restaurants so far in {city_name}...")
        time.sleep(1)  # Rate limiting
    
    return {
        'city': city_name,
        'state': city_data['state'],
        'restaurant_count': total_results,
        'restaurants': restaurants
    }

def main():
    """Main function to fetch restaurant data from Foursquare"""
    # Get API key from environment
    api_key = os.getenv('FOURSQUARE_API_KEY')
    if not api_key:
        raise ValueError("FOURSQUARE_API_KEY not found in environment variables")
    
    api = FoursquareAPI(api_key)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_restaurants': 0,
        'cities': []
    }
    
    # Create Results/4square directory if it doesn't exist
    os.makedirs('/opt/noogabites/Results/4square', exist_ok=True)
    
    for city_name, city_data in CITIES.items():
        # Add delay between cities
        if results['cities']:
            time.sleep(2)
            
        city_results = get_restaurants_for_city(api, city_name, city_data)
        results['cities'].append(city_results)
        results['total_restaurants'] += city_results['restaurant_count']
        
        # Save progress after each city
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        progress_file = f'/opt/noogabites/Results/4square/foursquare_progress_{timestamp}.json'
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Progress saved to: {progress_file}")
    
    # Save final results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'/opt/noogabites/Results/4square/foursquare_restaurant_data_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary:")
    print("-" * 50)
    print(f"Total restaurants found: {results['total_restaurants']}")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()
