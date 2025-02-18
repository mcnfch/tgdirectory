#!/usr/bin/env python3
import json
from pathlib import Path
from glob import glob
from collections import defaultdict

def load_foursquare_data():
    with open('/opt/noogabites/Results/restaurant_results.json', 'r') as f:
        data = json.load(f)
        restaurants = []
        for city in data['cities']:
            restaurants.extend(city['restaurants'])
        return restaurants

# Get all progress files
progress_files = glob('/opt/noogabites/Results/places_api_progress_*.json')
all_places = []
places_by_file = defaultdict(list)

# Load all places from all progress files
print("\nAnalyzing progress files:")
for file in progress_files:
    with open(file, 'r') as f:
        places = json.load(f)
        if isinstance(places, list):
            filename = Path(file).name
            places_by_file[filename] = places
            print(f"{filename}: {len(places)} places")
            all_places.extend(places)

# Get Foursquare data
foursquare_places = load_foursquare_data()
print(f"\nFoursquare restaurants: {len(foursquare_places)}")

# Remove duplicates based on place ID
unique_places = {}
duplicates = defaultdict(list)
for place in all_places:
    google_data = place.get('google_data', {})
    place_id = google_data.get('id')
    name = place.get('foursquare_data', {}).get('name', 'Unknown')
    if place_id:
        if place_id in unique_places:
            duplicates[place_id].append(name)
        unique_places[place_id] = place

print(f"\nGoogle Places API results:")
print(f"Total places across all files: {len(all_places)}")
print(f"Unique places after deduplication: {len(unique_places)}")
print(f"Number of duplicated places: {len(duplicates)}")

if duplicates:
    print("\nDuplicate entries found for:")
    for place_id, names in duplicates.items():
        original_name = unique_places[place_id]['foursquare_data'].get('name', 'Unknown')
        print(f"- {original_name} appeared in files with names: {', '.join(set(names))}")

total_places = len(unique_places)
places_with_photos = 0
total_photos = 0
photo_counts = []

for place_id, place in unique_places.items():
    google_data = place.get('google_data', {})
    photos = google_data.get('photos', [])
    name = place.get('foursquare_data', {}).get('name', 'Unknown')
    
    if photos:
        places_with_photos += 1
        total_photos += len(photos)
        photo_counts.append((name, len(photos)))

print(f"\nPhoto Analysis:")
print(f"Progress files analyzed: {len(progress_files)}")
print(f"Total unique places: {total_places}")
print(f"Places with photos: {places_with_photos} ({(places_with_photos/total_places)*100:.1f}%)")
print(f"Places without photos: {total_places - places_with_photos} ({((total_places-places_with_photos)/total_places)*100:.1f}%)")
print(f"Total photos across all places: {total_photos}")
if places_with_photos > 0:
    print(f"Average photos per place (for places with photos): {total_photos/places_with_photos:.1f}")

print("\nTop 10 places by number of photos:")
for name, count in sorted(photo_counts, key=lambda x: x[1], reverse=True)[:10]:
    print(f"- {name}: {count} photos")

print("\nPlaces without photos:")
for place_id, place in unique_places.items():
    if not place.get('google_data', {}).get('photos'):
        name = place.get('foursquare_data', {}).get('name', 'Unknown')
        print(f"- {name} (ID: {place_id})")
