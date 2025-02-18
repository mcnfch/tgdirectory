import json
import time
import os
from datetime import datetime
import requests

class VisitChatScraper:
    def __init__(self):
        self.base_url = "https://www.visitchattanooga.com/restaurants/"
        self.api_url = "https://www.visitchattanooga.com/includes/rest/plugins/listings/1/search"
        self.restaurants = []
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://www.visitchattanooga.com',
            'Referer': self.base_url
        }
        
    def get_restaurant_data(self, max_restaurants=500):
        """Get restaurant data directly using requests"""
        try:
            all_restaurants = []
            current_skip = 0
            page_size = 24
            
            while current_skip < max_restaurants:
                payload = {
                    "query": {
                        "categories.catid": "39",
                        "active": True,
                        "deleted": False
                    },
                    "options": {
                        "limit": page_size,
                        "skip": current_skip,
                        "sort": {
                            "qualityScore": -1,
                            "title": 1
                        },
                        "fields": {
                            "recid": 1,
                            "title": 1,
                            "description": 1,
                            "address1": 1,
                            "city": 1,
                            "state": 1,
                            "zip": 1,
                            "latitude": 1,
                            "longitude": 1,
                            "phone": 1,
                            "website": 1,
                            "weburl": 1,
                            "url": 1,
                            "primary_image_url": 1,
                            "qualityScore": 1,
                            "isDTN": 1,
                            "dtn": 1,
                            "primary_category": 1,
                            "taid": 1,
                            "listingudfs_object": 1
                        }
                    }
                }
                
                try:
                    print(f"\nFetching restaurants (skip={current_skip})...")
                    response = self.session.post(self.api_url, json=payload, headers=self.headers)
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data or not isinstance(data, dict):
                        print(f"Invalid response format on page {current_skip // page_size + 1}")
                        print(f"Response: {data}")
                        break
                        
                    # Handle both response formats we've seen
                    if 'docs' in data and isinstance(data['docs'], dict):
                        restaurants = data['docs'].get('docs', [])
                    elif 'docs' in data and isinstance(data['docs'], list):
                        restaurants = data['docs']
                    else:
                        restaurants = []
                        
                    if not restaurants:
                        print("No more restaurants found")
                        break
                        
                    for r in restaurants:
                        if isinstance(r, dict) and r.get('title'):
                            quality_score = r.get('qualityScore', 0)
                            dtn_status = "DTN" if r.get('isDTN') else "Regular"
                            print(f"Found: {r['title']} (Score: {quality_score}, {dtn_status})")
                            all_restaurants.append(r)
                            
                    if len(restaurants) < page_size:
                        print("Reached end of restaurant listings")
                        break
                        
                    current_skip += len(restaurants)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing page {current_skip // page_size + 1}: {str(e)}")
                    if hasattr(e, 'response'):
                        print(f"Response status: {e.response.status_code}")
                        print(f"Response text: {e.response.text[:500]}")
                    break
                    
            print(f"\nFound {len(all_restaurants)} total restaurants")
            self.restaurants = all_restaurants
            return all_restaurants
            
        except Exception as e:
            print(f"Error getting restaurant data: {str(e)}")
            return []
        
    def save_results(self, restaurants):
        """Save restaurant data to JSON file"""
        if not restaurants:
            print("No restaurants to save")
            return
            
        results_dir = "/opt/noogabites/Results/visitchat"
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"{results_dir}/restaurants_{timestamp}.json"
        
        sorted_restaurants = sorted(
            restaurants,
            key=lambda x: (
                x.get('isDTN', False),
                x.get('qualityScore', 0),
                x.get('dtn', {}).get('rank', 999),
                x.get('title', '')
            ),
            reverse=True
        )
        
        output_data = {
            "restaurants": sorted_restaurants,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "count": len(restaurants),
                "dtn_count": sum(1 for r in restaurants if r.get('isDTN')),
                "avg_quality_score": sum(r.get('qualityScore', 0) for r in restaurants) / len(restaurants) if restaurants else 0
            }
        }
            
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
            
        print(f"\nSaved {len(restaurants)} restaurants to {output_file}")

if __name__ == "__main__":
    scraper = VisitChatScraper()
    try:
        restaurants = scraper.get_restaurant_data(max_restaurants=500)
        if restaurants:
            scraper.save_results(restaurants)
        else:
            print("No restaurants found")
    except Exception as e:
        print(f"Error: {str(e)}")
