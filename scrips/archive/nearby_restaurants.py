import requests
import time
import json

# API key
api_key = 'AIzaSyBixueohHNSo3g1RvaU7myg1u1K7qiqlwc'

# Google Places API URL for Text Search
base_url = "https://places.googleapis.com/v1/places:searchText"

# Headers for Google Places API
headers = {
    'X-Goog-Api-Key': api_key,
    'Content-Type': 'application/json',
    'X-Goog-FieldMask': (
        'places.id,'
        'places.displayName,'
        'places.formattedAddress,'
        'places.location,'
        'places.rating,'
        'places.userRatingCount,'
        'places.internationalPhoneNumber,'
        'places.websiteUri,'
        'places.googleMapsUri'
    )
}

def get_restaurants(city_name):
    seen_ids = set()  # Track unique restaurant IDs
    unique_restaurants = []
    query = f"restaurants in {city_name}"
    
    # Make up to 3 requests to get up to 60 results
    for page in range(3):
        data = {
            "textQuery": query,
            "maxResultCount": 20
        }
        
        try:
            print(f"\nMaking request {page + 1} for {city_name}...")
            print(f"Query: {query}")
            
            # Make the API request
            response = requests.post(base_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            # Add new unique restaurants from this page
            new_restaurants = result.get('places', [])
            for restaurant in new_restaurants:
                if restaurant['id'] not in seen_ids:
                    seen_ids.add(restaurant['id'])
                    unique_restaurants.append(restaurant)
            
            print(f"Found {len(new_restaurants)} restaurants on page {page + 1}")
            print(f"Total unique restaurants so far: {len(unique_restaurants)}")
            
            # If we got less than maxResultCount results, no more pages available
            if len(new_restaurants) < 20:
                break
                
            # Add a small delay between requests
            time.sleep(2)
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if response.text:
                print("Response:", response.text)
            break
    
    return unique_restaurants

def main():
    # Search for restaurants in New York City
    city = "New York City, NY"
    restaurants = get_restaurants(city)
    
    # Print results
    print(f"\nFound {len(restaurants)} unique restaurants in {city}")
    print("-" * 50)
    
    for idx, restaurant in enumerate(restaurants, 1):
        name = restaurant['displayName']['text']
        address = restaurant['formattedAddress']
        rating = restaurant.get('rating', 'No rating')
        reviews = restaurant.get('userRatingCount', 0)
        website = restaurant.get('websiteUri', 'No website')
        
        print(f"{idx}. {name}")
        print(f"   Address: {address}")
        print(f"   Rating: {rating}/5 ({reviews} reviews)")
        print(f"   Website: {website}")
        print()

if __name__ == "__main__":
    main()
