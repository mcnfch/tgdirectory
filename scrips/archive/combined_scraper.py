#!/usr/bin/env python3
import json
from datetime import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import traceback
from listing import setup_driver, extract_additional_info

def load_osm_restaurants(filename):
    """Load restaurants from OSM results file"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('restaurants', [])

def construct_google_maps_url(restaurant_name, city):
    """Construct Google Maps search URL for a restaurant"""
    search_query = f"{restaurant_name} {city}".replace(' ', '+')
    return f"https://www.google.com/maps/search/{search_query}/"

def scrape_restaurant_details(driver, restaurants, city):
    """Scrape additional details from Google Maps for each restaurant"""
    results = []
    
    for i, restaurant in enumerate(restaurants, 1):
        name = restaurant['name']
        if name == "Unknown":
            continue
            
        print(f"\nProcessing {i}/{len(restaurants)}: {name}")
        
        try:
            url = construct_google_maps_url(name, city)
            additional_info = extract_additional_info(driver, url, name)
            
            result = {
                "osm_name": name,
                "osm_cuisine": restaurant.get("cuisine", "Not specified"),
                "google_maps_data": additional_info
            }
            
            results.append(result)
            
            # Save progress periodically
            if i % 10 == 0:
                save_results(results, city, "progress")
                
            # Add delay between requests to avoid rate limiting
            time.sleep(5)
            
        except Exception as e:
            print(f"Error processing {name}: {str(e)}")
            traceback.print_exc()
            continue
    
    return results

def save_results(results, city, suffix="final"):
    """Save results to a JSON file"""
    if not os.path.exists("Results"):
        os.makedirs("Results")
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Results/combined_restaurants_{city.lower()}_{suffix}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"restaurants": results}, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(results)} restaurants to {filename}")

def main():
    # Load the most recent OSM results file
    results_dir = "Results"
    osm_files = [f for f in os.listdir(results_dir) if f.startswith("osm_restaurants_simple_")]
    if not osm_files:
        print("No OSM restaurant files found!")
        return
        
    latest_file = max(osm_files, key=lambda x: os.path.getmtime(os.path.join(results_dir, x)))
    osm_filepath = os.path.join(results_dir, latest_file)
    print(f"Loading restaurants from {osm_filepath}")
    
    restaurants = load_osm_restaurants(osm_filepath)
    print(f"Loaded {len(restaurants)} restaurants from OSM data")
    
    # Setup the web driver
    driver = setup_driver()
    
    try:
        # Scrape additional details from Google Maps
        results = scrape_restaurant_details(driver, restaurants, "Chattanooga")
        
        # Save final results
        save_results(results, "Chattanooga")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
