#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import os

def get_restaurants_from_osm(bbox):
    """
    Get restaurants from OpenStreetMap using Overpass API
    bbox: tuple of (south, west, north, east) coordinates
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="restaurant"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      way["amenity"="restaurant"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      relation["amenity"="restaurant"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out body;
    >;
    out skel qt;
    """
    
    print("Fetching restaurants from OpenStreetMap...")
    response = requests.post(overpass_url, data={"data": overpass_query})
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        return []
    
    data = response.json()
    restaurants = []
    
    for element in data.get("elements", []):
        if element.get("type") in ["node", "way", "relation"]:
            tags = element.get("tags", {})
            if tags.get("amenity") == "restaurant":
                restaurant = {
                    "name": tags.get("name", "Unknown"),
                    "cuisine": tags.get("cuisine", "Not specified")
                }
                restaurants.append(restaurant)
    
    return restaurants

def save_results(restaurants, city):
    """Save results to a JSON file"""
    if not os.path.exists("Results"):
        os.makedirs("Results")
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Results/osm_restaurants_simple_{city.lower()}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"restaurants": restaurants}, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(restaurants)} restaurants to {filename}")

def main():
    # Chattanooga bbox (approximately)
    # Format: (south, west, north, east)
    chattanooga_bbox = (35.0, -85.4, 35.2, -85.2)
    
    restaurants = get_restaurants_from_osm(chattanooga_bbox)
    print(f"Found {len(restaurants)} restaurants")
    
    if restaurants:
        save_results(restaurants, "chattanooga")

if __name__ == "__main__":
    main()
