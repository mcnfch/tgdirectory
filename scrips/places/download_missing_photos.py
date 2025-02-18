#!/usr/bin/env python3
import os
import json
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
BASE_IMAGE_DIR = Path('/opt/noogabites/public/images')
MISSING_IDS_FILE = Path('/opt/noogabites/Reconcile/photos/missing_photo_ids.txt')

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_place_details(place_id):
    """Get fresh place details from Places API"""
    url = f"https://places.googleapis.com/v1/places/{place_id}?fields=id,displayName,photos"
    headers = {
        'X-Goog-Api-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting details for place {place_id}: {str(e)}")
        return None

def download_photo(place_id, photo_ref, index, save_dir):
    """Download a single photo from Google Places API"""
    url = f"https://places.googleapis.com/v1/places/{place_id}/photos/{photo_ref}/media"
    headers = {'X-Goog-Api-Key': API_KEY}
    params = {'maxWidthPx': 800, 'maxHeightPx': 600}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # Save the photo
        photo_path = save_dir / f"photo_{index + 1}.jpg"
        with open(photo_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved {photo_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading photo {index + 1} for place {place_id}: {str(e)}")
        return False

def main():
    # Ensure base directory exists
    ensure_directory(BASE_IMAGE_DIR)
    
    # Load the missing IDs from file
    with open(MISSING_IDS_FILE, 'r') as f:
        missing_ids = [line.strip() for line in f if line.strip()]
    
    total_photos = 0
    successful_photos = 0
    
    print(f"Processing {len(missing_ids)} missing places...")
    
    # Process each missing place ID
    for place_id in missing_ids:
        # Get fresh place details
        place_data = get_place_details(place_id)
        if not place_data:
            print(f"Could not get details for place {place_id}")
            continue
            
        photos = place_data.get('photos', [])
        name = place_data.get('displayName', {}).get('text', 'Unknown')
        
        if not photos:
            print(f"No photos found for {name} ({place_id})")
            continue
            
        # Create directory for this place
        place_dir = ensure_directory(BASE_IMAGE_DIR / place_id)
        print(f"\nProcessing {name} ({place_id}) - {len(photos)} photos")
        
        # Download each photo
        for i, photo in enumerate(photos):
            photo_ref = photo.get('name', '').split('/')[-1]
            total_photos += 1
            if download_photo(place_id, photo_ref, i, place_dir):
                successful_photos += 1
            time.sleep(0.5)  # Be nice to the API
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded {successful_photos} out of {total_photos} photos")

if __name__ == "__main__":
    main()
