import json
import os

# Read the files
with open('/opt/tgdirectory/src/data/static/live_data.json', 'r') as f:
    live_data = json.load(f)

with open('/opt/tgdirectory/src/data/static/places_districts.json', 'r') as f:
    places_districts = json.load(f)

# Update districts in live_data
for place_id, district in places_districts['places_to_districts'].items():
    if place_id in live_data['restaurants']:
        # Update district and remove district_description
        live_data['restaurants'][place_id]['description'] = ""
        live_data['restaurants'][place_id]['district'] = district
        if 'district_description' in live_data['restaurants'][place_id]:
            del live_data['restaurants'][place_id]['district_description']

# Create backup of original file
backup_path = '/opt/tgdirectory/src/data/static/live_data.json.bak'
os.rename('/opt/tgdirectory/src/data/static/live_data.json', backup_path)

# Write updated data
with open('/opt/tgdirectory/src/data/static/live_data.json', 'w') as f:
    json.dump(live_data, f, indent=2)

print(f"Updated live_data.json with new districts")
print(f"Original file backed up to {backup_path}")
