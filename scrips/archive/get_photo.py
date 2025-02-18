#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
PLACE_ID = "ChIJbSPROnleYIgRvSxISw3t36U"
PHOTO_REF = "AVzFdbnJurDByqYXAq50gTrqGwomHlV9Wizo01r7cLvhyqGuNHDEWLS8F6TEmshbUrxFJ3-NSOc8z8Vu88OCZCeoFezZPo1kO0eybMW97GjYs7LxezTt6A4FznLHZaP58_fSNVB4J_0cf0JJTuIgeabrllz7s2iyA1mS6vFO"

url = f"https://places.googleapis.com/v1/places/{PLACE_ID}/photos/{PHOTO_REF}/media"
headers = {
    'X-Goog-Api-Key': API_KEY
}
params = {
    'maxWidthPx': 800,  # Requesting a reasonable size
    'maxHeightPx': 600
}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    # Save the photo
    with open('restaurant_photo.jpg', 'wb') as f:
        f.write(response.content)
    print("Photo saved as restaurant_photo.jpg")
except requests.exceptions.RequestException as e:
    print(f"Error getting photo: {str(e)}")
    if hasattr(e.response, 'text'):
        print(f"Response: {e.response.text}")
