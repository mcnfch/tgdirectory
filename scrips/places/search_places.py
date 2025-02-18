import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')

def search_place(place_name):
    """Search for a specific place and return its formatted data"""
    print(f"\nSearching for {place_name} with all available fields...")
    search_url = 'https://places.googleapis.com/v1/places:searchText'
    
    # Comprehensive field mask for all available data
    fields = [
        'places.id',
        'places.displayName',
        'places.formattedAddress',
        'places.addressComponents',
        'places.location',
        'places.viewport',
        'places.types',
        'places.businessStatus',
        'places.primaryType',
        'places.primaryTypeDisplayName',
        'places.rating',
        'places.userRatingCount',
        'places.googleMapsUri',
        'places.websiteUri',
        'places.internationalPhoneNumber',
        'places.nationalPhoneNumber',
        'places.currentOpeningHours',
        'places.regularOpeningHours',
        'places.priceLevel',
        'places.photos',
        'places.delivery',
        'places.dineIn',
        'places.takeout',
        'places.curbsidePickup',
        'places.reservable',
        'places.servesBeer',
        'places.servesWine',
        'places.servesCocktails',
        'places.servesVegetarianFood',
        'places.outdoorSeating',
        'places.reviews',
        'places.parkingOptions',
        'places.paymentOptions',
        'places.accessibilityOptions'
    ]
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': ','.join(fields)
    }
    
    data = {
        'textQuery': place_name
    }
    
    try:
        search_response = requests.post(search_url, headers=headers, json=data)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if 'places' in search_data and search_data['places']:
            place = search_data['places'][0]
            formatted_data = format_place_data(place)
            
            print(f"Found {place_name}!")
            print(f"Name: {formatted_data['google_data']['displayName']}")
            print(f"Address: {formatted_data['google_data']['formattedAddress']}")
            print(f"Rating: {formatted_data['google_data']['rating']}/5 ({formatted_data['google_data']['userRatingCount']} reviews)")
            print(f"Status: {formatted_data['google_data']['businessStatus']}")
            
            if 'currentOpeningHours' in place:
                print("\nCurrent Hours:")
                for period in place['currentOpeningHours'].get('weekdayDescriptions', []):
                    print(f"  {period}")
            
            if formatted_data['google_data']['photos']:
                print(f"\nPhotos Available: {len(formatted_data['google_data']['photos'])}")
                print("Photo URLs:")
                for i, photo in enumerate(formatted_data['google_data']['photos'], 1):
                    print(f"  Photo {i}:")
                    print(f"    URL: {photo['url']}")
                    print(f"    Width: {photo['width']}px")
                    print(f"    Height: {photo['height']}px")
            
            # Save the result
            output_dir = '/opt/noogabites/Results/places'
            os.makedirs(output_dir, exist_ok=True)
            
            # Use place ID for filename if available
            place_id = formatted_data['google_data'].get('id', '')
            if place_id:
                filename = f"{place_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                # Fallback to sanitized place name if no ID
                safe_name = "".join(c for c in place_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
            output_file = os.path.join(output_dir, filename)
            with open(output_file, 'w') as f:
                json.dump(formatted_data, f, indent=2)
            print(f"\nSaved detailed results to {output_file}")
            return formatted_data
        else:
            print(f"No places found for {place_name}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def format_place_data(place):
    """Format place data into our desired structure"""
    return {
        "google_data": {
            "id": place.get('id'),
            "googleMapsUri": place.get('googleMapsUri'),
            "businessStatus": place.get('businessStatus'),
            "userRatingCount": place.get('userRatingCount'),
            "rating": place.get('rating'),
            "displayName": place.get('displayName', {}).get('text'),
            "formattedAddress": place.get('formattedAddress'),
            "internationalPhoneNumber": place.get('internationalPhoneNumber'),
            "nationalPhoneNumber": place.get('nationalPhoneNumber'),
            "currentOpeningHours": place.get('currentOpeningHours'),
            "regularOpeningHours": place.get('regularOpeningHours'),
            "websiteUri": place.get('websiteUri'),
            "priceLevel": place.get('priceLevel'),
            "photos": transform_photo_references(place),
            "location": place.get('location'),
            "types": place.get('types'),
            "dineIn": place.get('dineIn'),
            "takeout": place.get('takeout'),
            "delivery": place.get('delivery'),
            "curbsidePickup": place.get('curbsidePickup'),
            "reservable": place.get('reservable'),
            "outdoorSeating": place.get('outdoorSeating'),
            "servesCocktails": place.get('servesCocktails'),
            "paymentOptions": place.get('paymentOptions')
        }
    }

def transform_photo_references(place_data):
    """Transform photo data into a list of photo URLs"""
    photos = []
    if 'photos' in place_data:
        for photo in place_data['photos']:
            if 'photo_reference' in photo:
                photo_info = {
                    'reference': photo['photo_reference'],
                    'url': get_photo_url(photo['photo_reference'], photo.get('widthPx')),
                    'width': photo.get('widthPx', 800),
                    'height': photo.get('heightPx', 600)
                }
                photos.append(photo_info)
    return photos

def get_photo_url(photo_reference, max_width=None):
    """Get the proper photo URL using the Places API (New)"""
    base_url = "https://places.googleapis.com/v1"
    url = f"{base_url}/{photo_reference}/media?key={API_KEY}"
    if max_width:
        url += f"&maxWidthPx={max_width}"
    return url

def main():
    # Load the visit data JSON
    visit_data_file = '/opt/noogabites/public/data/visit_data_20250215_191520_full.json'
    try:
        with open(visit_data_file, 'r') as f:
            visit_data = json.load(f)
        
        # Extract unique restaurant names from the restaurants array
        restaurant_names = set()
        if 'restaurants' in visit_data:
            for restaurant in visit_data['restaurants']:
                if 'title' in restaurant:
                    restaurant_names.add(restaurant['title'])
        
        print(f"Found {len(restaurant_names)} unique restaurants to process")
        
        # Process each restaurant
        for i, restaurant in enumerate(sorted(restaurant_names), 1):
            print(f"\nProcessing restaurant {i}/{len(restaurant_names)}")
            search_place(restaurant)
            # Add a small delay between requests to avoid rate limiting
            time.sleep(2)
            
    except FileNotFoundError:
        print(f"Error: Could not find visit data file at {visit_data_file}")
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from {visit_data_file}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()
