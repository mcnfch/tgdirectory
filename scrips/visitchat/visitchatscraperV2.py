import json
import time
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class VisitChatScraper:
    def __init__(self):
        self.base_url = "https://www.visitchattanooga.com/restaurants/"
        self.api_url = "https://www.visitchattanooga.com/includes/rest/plugins/listings/public/listings/search"
        self.restaurants = []
        self.session = requests.Session()
        
        # Set up headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://www.visitchattanooga.com',
            'Referer': 'https://www.visitchattanooga.com/restaurants/'
        }
        
    def get_initial_data(self):
        """Get initial data from the restaurants page"""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the script tag containing the initial data
            for script in soup.find_all('script'):
                if script.string and 'window.__INITIAL_STATE__' in script.string:
                    data = script.string
                    start = data.find('{')
                    end = data.rfind('}') + 1
                    if start > -1 and end > 0:
                        initial_data = json.loads(data[start:end])
                        return initial_data
            return None
        except Exception as e:
            print(f"Error getting initial data: {str(e)}")
            return None
        
    def get_restaurant_data(self, max_restaurants=500):
        """Get all restaurant data using their new API structure"""
        try:
            print("\nStarting restaurant data collection...")
            all_restaurants = []
            current_skip = 0
            page_size = 24
            
            # Get initial data first
            initial_data = self.get_initial_data()
            if not initial_data:
                print("Could not get initial data")
                return []
            
            # Extract necessary information from initial data
            try:
                token = initial_data.get('auth', {}).get('token')
                if token:
                    self.headers['Authorization'] = f'Bearer {token}'
            except:
                pass
            
            while current_skip < max_restaurants:
                # Set up the request payload
                payload = {
                    "query": {
                        "categories.catid": "5f6a346e8a0b5b1feb9c6766",  # Restaurant category
                        "active": True,
                        "deleted": False
                    },
                    "options": {
                        "limit": page_size,
                        "skip": current_skip,
                        "sort": {
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
                            "rankorder": 1,
                            "categories": 1
                        }
                    }
                }
                
                try:
                    response = self.session.post(self.api_url, json=payload, headers=self.headers)
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data or not isinstance(data, dict):
                        print(f"Invalid response format on page {current_skip // page_size + 1}")
                        break
                        
                    restaurants = data.get('docs', [])
                    if not restaurants:
                        print("No more restaurants found")
                        break
                        
                    for r in restaurants:
                        if isinstance(r, dict) and r.get('title'):
                            print(f"Found: {r['title']}")
                            all_restaurants.append(r)
                            
                    if len(restaurants) < page_size:
                        print("Reached end of restaurant listings")
                        break
                        
                    current_skip += len(restaurants)
                    time.sleep(1)  # Be nice to their server
                    
                except Exception as e:
                    print(f"Error processing page {current_skip // page_size + 1}: {str(e)}")
                    if hasattr(e, 'response'):
                        print(f"Response status: {e.response.status_code}")
                        print(f"Response text: {e.response.text[:500]}")  # Print first 500 chars of error
                    break
                    
            print(f"\nFound {len(all_restaurants)} total restaurants")
            self.restaurants = all_restaurants
            return all_restaurants
            
        except Exception as e:
            print(f"Error getting restaurant data: {str(e)}")
            return []

    def save_results(self, restaurants, include_raw=False):
        """Save restaurant data to JSON file"""
        if not restaurants:
            print("No restaurants to save")
            return
            
        # Create Results directory if it doesn't exist
        results_dir = "/opt/noogabites/Results/visitchat"
        os.makedirs(results_dir, exist_ok=True)
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"{results_dir}/restaurants_{timestamp}.json"
        
        output_data = {
            "restaurants": restaurants,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "count": len(restaurants)
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