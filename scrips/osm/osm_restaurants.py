#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime
from typing import Dict, List
import overpy

def load_cities() -> List[Dict]:
    """Load cities from JSON file"""
    with open('/opt/noogabites/public/data/cities.json', 'r') as f:
        return json.load(f)

def build_overpass_query(city_data: Dict[str, float], radius_km: float = 5) -> str:
    """
    Build Overpass QL query for restaurants within radius of city center
    """
    lat, lon = city_data['lat'], city_data['lon']
    radius_meters = radius_km * 1000
    return f"""
        area[name="United States"][admin_level=2]->.country;
        (
          node["amenity"="restaurant"](area.country)(around:{radius_meters},{lat},{lon});
          way["amenity"="restaurant"](area.country)(around:{radius_meters},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
    """

def extract_tags(tags: Dict) -> Dict:
    """Extract relevant tags from OSM element"""
    tag_mapping = {
        'name': ['name', 'name:en'],
        'cuisine': ['cuisine'],
        'phone': ['phone', 'contact:phone', 'phone:contact'],
        'website': ['website', 'contact:website', 'url'],
        'opening_hours': ['opening_hours'],
        'addr:street': ['addr:street', 'address:street'],
        'addr:housenumber': ['addr:housenumber', 'house_number'],
        'addr:city': ['addr:city', 'city'],
        'addr:state': ['addr:state', 'state'],
        'addr:postcode': ['addr:postcode', 'postal_code'],
        'takeaway': ['takeaway'],
        'delivery': ['delivery'],
        'outdoor_seating': ['outdoor_seating'],
        'wheelchair': ['wheelchair'],
        'diet:vegetarian': ['diet:vegetarian', 'vegetarian'],
        'diet:vegan': ['diet:vegan', 'vegan'],
        'payment:credit_cards': ['payment:credit_cards', 'credit_cards'],
        'internet_access': ['internet_access', 'wifi'],
        'smoking': ['smoking'],
        'drive_through': ['drive_through', 'drive_thru'],
        'level': ['level'],
        'brand': ['brand'],
        'operator': ['operator'],
        'description': ['description'],
        'cuisine_1': ['cuisine:1'],
        'cuisine_2': ['cuisine:2'],
        'reservation': ['reservation'],
        'capacity': ['capacity', 'seats'],
        'microbrewery': ['microbrewery'],
        'brewery': ['brewery']
    }
    
    result = {}
    for key, possible_tags in tag_mapping.items():
        for tag in possible_tags:
            if tag in tags:
                result[key] = tags[tag]
                break
        if key not in result:
            result[key] = ''
    
    return result

def get_restaurants_for_city(city_name: str, city_data: Dict) -> Dict:
    """Get restaurant data for a city using Overpass API"""
    print(f"Fetching restaurants for {city_name}...")
    
    try:
        api = overpy.Overpass()
        query = build_overpass_query({
            'lat': city_data['location']['latitude'],
            'lon': city_data['location']['longitude']
        })
        result = api.query(query)
        
        restaurants = []
        
        # Process nodes (standalone restaurants)
        for node in result.nodes:
            restaurants.append({
                'osm_id': node.id,
                'osm_type': 'node',
                'latitude': float(node.lat),
                'longitude': float(node.lon),
                'tags': extract_tags(node.tags)
            })
        
        # Process ways (buildings)
        for way in result.ways:
            if way.nodes:  # Calculate center point from nodes
                lat = sum(float(n.lat) for n in way.nodes) / len(way.nodes)
                lon = sum(float(n.lon) for n in way.nodes) / len(way.nodes)
                restaurants.append({
                    'osm_id': way.id,
                    'osm_type': 'way',
                    'latitude': lat,
                    'longitude': lon,
                    'tags': extract_tags(way.tags)
                })
        
        print(f"Found {len(restaurants)} restaurants in {city_name}")
        return {
            'city_name': city_name,
            'state': city_data['state'],
            'latitude': city_data['location']['latitude'],
            'longitude': city_data['location']['longitude'],
            'restaurants': restaurants
        }
        
    except Exception as e:
        print(f"Error fetching data for {city_name}: {str(e)}")
        return {
            'city_name': city_name,
            'state': city_data['state'],
            'latitude': city_data['location']['latitude'],
            'longitude': city_data['location']['longitude'],
            'restaurants': []
        }

def main():
    # Create results directory if it doesn't exist
    results_dir = '/opt/noogabites/Results/osm'
    os.makedirs(results_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(results_dir, f'osm_restaurant_data_{timestamp}.json')
    
    # Load cities
    cities = load_cities()
    
    # Collect restaurant data for each city
    results = []
    for city_data in cities:
        city_name = city_data['name']
        result = get_restaurants_for_city(city_name, city_data)
        results.append(result)
        
        # Save after each city in case of interruption
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Rate limiting
        time.sleep(5)
    
    print(f"\nResults saved to {output_file}")

if __name__ == '__main__':
    main()
