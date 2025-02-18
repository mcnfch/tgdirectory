#!/usr/bin/env python3
import os
import json
import time
import requests
from dotenv import load_dotenv
from pathlib import Path
from glob import glob

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
BASE_IMAGE_DIR = Path('/opt/noogabites/public/images')

# Skip the first progress file we already processed
PROCESSED_FILE = '20250211_232342'
PROGRESS_FILES = [f for f in glob('/opt/noogabites/Results/places_api_progress_*.json') 
                 if PROCESSED_FILE not in f]

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def download_photo(place_id, photo_ref, index, save_dir):
    """Download a single photo from Google Places API"""
    # Extract just the photo reference from the full path
    photo_ref = photo_ref.split('photos/')[-1].split('/')[0]
    
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
    
    total_photos = 0
    successful_photos = 0
    
    print(f"Processing {len(PROGRESS_FILES)} remaining progress files...")
    
    # Process each progress file
    for progress_file in PROGRESS_FILES:
        print(f"\nProcessing file: {os.path.basename(progress_file)}")
        with open(progress_file, 'r') as f:
            places = json.load(f)
        
        # Process each place
        for place in places:
            google_data = place.get('google_data', {})
            place_id = google_data.get('id')
            photos = google_data.get('photos', [])
            name = place.get('foursquare_data', {}).get('name', 'Unknown')
            
            if not place_id or not photos:
                continue
                
            # Skip if we already have photos for this place
            place_dir = BASE_IMAGE_DIR / place_id
            if place_dir.exists() and any(place_dir.iterdir()):
                print(f"Skipping {name} - photos already downloaded")
                continue
                
            # Create directory for this place
            place_dir = ensure_directory(place_dir)
            print(f"\nProcessing {name} ({place_id}) - {len(photos)} photos")
            
            # Download each photo
            for i, photo_ref in enumerate(photos):
                total_photos += 1
                if download_photo(place_id, photo_ref, i, place_dir):
                    successful_photos += 1
                time.sleep(0.5)  # Be nice to the API
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded {successful_photos} out of {total_photos} photos")

if __name__ == "__main__":
    main()
