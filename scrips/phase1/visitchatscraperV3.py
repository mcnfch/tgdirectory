#!/usr/bin/env python3
import json
import time
import os
import threading
import signal
from datetime import datetime
from pychrome import Browser

class ResponseDumper:
    def __init__(self):
        self.base_url = "https://www.visitchattanooga.com"
        self.api_url = f"{self.base_url}/includes/rest_v2/plugins_listings_listings/find/"
        self.browser = Browser(url="http://127.0.0.1:9222")
        self.tab = self.browser.new_tab()
        self.output_dir = '/opt/noogabites/Results/visitchat'
        self.all_restaurants = []
        self.running = True
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Enable required domains
        self.tab.start()
        self.tab.Network.enable()
        self.tab.Page.enable()

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\nReceived shutdown signal. Cleaning up...")
        self.running = False
        self.cleanup()

    def cleanup(self):
        """Clean up browser resources"""
        try:
            self.tab.Network.disable()
            self.tab.Page.disable()
            self.tab.stop()
            self.browser.close_tab(self.tab)
        except:
            pass

    def handle_response(self, **kwargs):
        """Handle network responses by dumping them to files"""
        if not self.running:
            return
            
        response = kwargs.get('response', {})
        request_id = kwargs.get('requestId')
        url = response.get('url', '')
        
        if 'plugins_listings_listings/find' in url:
            print(f"Found restaurant data response: {url}")
            try:
                result = self.tab.Network.getResponseBody(requestId=request_id)
                if result and 'body' in result:
                    # Parse JSON data
                    data = json.loads(result['body'])
                    if 'docs' in data and 'docs' in data['docs']:
                        self.all_restaurants.extend(data['docs']['docs'])
                        
                        # If this is the first page, get total count and fetch remaining
                        if 'count' in data['docs']:
                            total = data['docs']['count']
                            skip = len(self.all_restaurants)
                            
                            # Only continue if we have more to fetch and we're still running
                            if skip < total and self.running:
                                print(f"Fetching more restaurants ({skip}/{total})...")
                                # Get the request parameters from URL
                                import urllib.parse
                                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                                if 'json' in parsed:
                                    params = json.loads(parsed['json'][0])
                                    # Remove any $nin filter
                                    if 'filter' in params and '$and' in params['filter']:
                                        params['filter']['$and'] = [f for f in params['filter']['$and'] if '$nin' not in str(f)]
                                    params['options']['skip'] = skip
                                    params['options']['limit'] = 100
                                    params['options']['sort'] = {"qualityScore": -1, "sortcompany": 1}
                                    # Make new request
                                    new_url = f"{self.api_url}?json={json.dumps(params)}&token={parsed['token'][0]}"
                                    
                                    # Add throttling delay
                                    time.sleep(3)  # Wait 3 seconds between requests
                                    
                                    self.tab.Page.navigate(url=new_url)
                                    # Wait for navigation and response
                                    time.sleep(2)
            except Exception as e:
                print(f"Error processing response: {str(e)}")

    def save_results(self):
        """Save all collected restaurants to a single file"""
        if self.all_restaurants:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"restaurants_{timestamp}_full.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump({
                    "count": len(self.all_restaurants),
                    "restaurants": self.all_restaurants
                }, f, indent=2)
            print(f"Saved {len(self.all_restaurants)} restaurants to {filepath}")

    def run(self):
        """Run the response dumper"""
        print(f"Loading restaurant listings page...")
        
        try:
            # Set up response handler
            self.tab.Network.responseReceived = self.handle_response
            
            # Create a simpler initial query that gets all restaurants
            initial_params = {
                "filter": {
                    "$and": [
                        {
                            "filter_tags": {
                                "$in": [
                                    "site_primary20_subcatid_104",  # American
                                    "site_primary20_subcatid_106",  # Asian
                                    "site_primary20_subcatid_108",  # Bakery/Ice Cream/Sweets
                                    "site_primary20_subcatid_111",  # BBQ
                                    "site_primary20_subcatid_114",  # Breakfast
                                    "site_primary20_subcatid_116",  # Casual Dining
                                    "site_primary20_subcatid_120",  # Deli & Sandwiches
                                    "site_primary20_subcatid_122",  # Desserts
                                    "site_primary20_subcatid_126",  # Family Dining
                                    "site_primary20_subcatid_127",  # Fast Food
                                    "site_primary20_subcatid_128",  # Fine Dining
                                    "site_primary20_subcatid_135",  # Italian
                                    "site_primary20_subcatid_138",  # Mexican
                                    "site_primary20_subcatid_139",  # Pizza
                                    "site_primary20_subcatid_145",  # Seafood
                                    "site_primary20_subcatid_147",  # Southern
                                    "site_primary20_subcatid_148",  # Specialty
                                    "site_primary20_subcatid_150",  # Steakhouse
                                    "site_primary20_subcatid_151",  # Sushi
                                    "site_primary20_subcatid_612",  # Indian
                                    "site_primary20_subcatid_633",  # Mediterranean
                                    "site_primary20_subcatid_634",  # Middle Eastern
                                    "site_primary20_subcatid_650",  # Sports Bar
                                    "site_primary20_subcatid_720",  # Pub Food
                                    "site_primary20_subcatid_723",  # Tapas
                                    "site_primary20_subcatid_757",  # Food Truck
                                    "site_primary20_subcatid_786",  # Burgers
                                    "site_primary20_subcatid_800",  # Coffee & Tea
                                    "site_primary20_subcatid_801",  # Contemporary
                                    "site_primary20_subcatid_804",  # Cajun
                                    "site_primary20_subcatid_805",  # Spanish
                                    "site_primary20_subcatid_806",  # Seafood Market
                                    "site_primary20_subcatid_807",  # Brazilian
                                    "site_primary20_subcatid_808",  # Farm to Table
                                    "site_primary20_subcatid_809",  # Ramen
                                    "site_primary20_subcatid_810",  # Hawaiian
                                    "site_primary20_subcatid_811",  # Donuts
                                    "site_primary20_subcatid_837"   # Brewery
                                ]
                            }
                        }
                    ]
                },
                "options": {
                    "limit": 100,
                    "skip": 0,
                    "count": True,
                    "sort": {"qualityScore": -1, "sortcompany": 1},
                    "fields": {
                        "recid": 1,
                        "title": 1,
                        "primary_category": 1,
                        "address1": 1,
                        "url": 1,
                        "isDTN": 1,
                        "latitude": 1,
                        "longitude": 1,
                        "primary_image_url": 1,
                        "qualityScore": 1,
                        "weburl": 1,
                        "listingudfs_object": 1,
                        "taid": 1,
                        "dtn.rank": 1,
                        "yelp.rating": 1,
                        "yelp.url": 1,
                        "yelp.review_count": 1,
                        "yelp.price": 1
                    }
                }
            }
            
            # Make initial request
            initial_url = f"{self.api_url}?json={json.dumps(initial_params)}&token=13a24b9818ea1e2d09c95ede1270bc3c"
            self.tab.Page.navigate(url=initial_url)
            
            # Wait for initial data to load
            time.sleep(15)
            
            # Wait for all requests to complete
            time.sleep(5)
            
            # Save all collected results
            self.save_results()
            
        except Exception as e:
            print(f"Error during execution: {str(e)}")
        finally:
            self.running = False
            time.sleep(2)  # Give time for pending requests
            self.cleanup()
            print("Finished capturing responses")

def main():
    dumper = ResponseDumper()
    dumper.run()

if __name__ == "__main__":
    main()
