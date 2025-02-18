#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('FOURSQUARE_API_KEY')

def search_place(query: str, near: str = "Chattanooga"):
    """
    Search for a specific place using Foursquare API
    
    Args:
        query: Name of the place to search for
        near: Location to search in, defaults to Chattanooga
    """
    url = "https://api.foursquare.com/v3/places/search"
    
    headers = {
        "Accept": "application/json",
        "Authorization": API_KEY
    }
    
    params = {
        "query": query,
        "near": near,
        "limit": 50,  # Get more results to ensure we find exact match
        "fields": "name,location,categories,rating,stats,tel,website"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        results = response.json()
        
        if 'results' in results:
            # First try to find exact match
            exact_matches = [place for place in results['results'] 
                           if place.get('name', '').lower() == query.lower()]
            
            if exact_matches:
                places = exact_matches
            else:
                # If no exact match, find places that contain the query
                places = [place for place in results['results'] 
                         if query.lower() in place.get('name', '').lower()]
            
            if not places:
                print(f"No places found matching '{query}'")
                return
                
            for place in places:
                print("\nFound place:")
                print(f"Name: {place.get('name', 'N/A')}")
                
                location = place.get('location', {})
                address_parts = []
                if 'address' in location:
                    address_parts.append(location['address'])
                if 'locality' in location:
                    address_parts.append(location['locality'])
                if 'region' in location:
                    address_parts.append(location['region'])
                if 'postcode' in location:
                    address_parts.append(location['postcode'])
                    
                print(f"Address: {', '.join(address_parts)}")
                print(f"Categories: {', '.join(cat.get('name', '') for cat in place.get('categories', []))}")
                
                if place.get('rating'):
                    print(f"Rating: {place.get('rating', 'N/A')}/10")
                if place.get('stats', {}).get('total_tips'):
                    print(f"Number of Reviews: {place['stats']['total_tips']}")
                if place.get('tel'):
                    print(f"Phone: {place['tel']}")
                if place.get('website'):
                    print(f"Website: {place['website']}")
        else:
            print("No results found")
            
    except requests.exceptions.RequestException as e:
        print(f"Error searching: {str(e)}")

def main():
    search_place("The FEED Co Table & Tavern")

if __name__ == "__main__":
    main()
