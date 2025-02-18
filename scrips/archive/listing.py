import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import traceback
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def setup_driver():
    """Setup and return a configured Chrome WebDriver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Wait for an element to be present and return it"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {selector}")
        return None

def scroll_panel_with_page_down(driver, panel_xpath, presses, pause_time):
    """
    Scrolls within a specific panel by simulating Page Down key presses.
    """
    try:
        # Find the panel element
        panel_element = driver.find_element(By.XPATH, panel_xpath)
        
        # Ensure the panel is in focus by clicking on it
        actions = ActionChains(driver)
        actions.move_to_element(panel_element).click().perform()
        
        # Send the Page Down key to the panel element
        for _ in range(presses):
            actions = ActionChains(driver)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(pause_time)
    except Exception as e:
        print(f"Error during scrolling: {str(e)}")

def extract_additional_info(driver, url, restaurant_name):
    """Extract additional information from a restaurant's individual page"""
    additional_info = {
        "phone": "",
        "website": "",
        "menu": "",
        "features": [],
        "hours": {},
        "price_range": "",
        "price_details": {},
        "address": "",
        "plus_code": "",
        "about": "",
        "categories": {
            "Accessibility": [],
            "Service options": [],
            "Highlights": [],
            "Popular for": [],
            "Offerings": [],
            "Dining options": [],
            "Amenities": [],
            "Atmosphere": [],
            "Crowd": [],
            "Planning": [],
            "Payments": [],
            "Parking": [],
            "Pets": []
        }
    }
    
    try:
        print(f"Loading page for {restaurant_name}...")
        
        # Set custom headers to appear more browser-like
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Load the page
        driver.get(url)
        
        # Wait for page to load with better timeout handling
        driver.implicitly_wait(30)
        time.sleep(5)  # Initial wait for JavaScript content
        
        # Save page source for debugging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_dir = '/opt/google-map-data/data/restaurant_pages'
        os.makedirs(html_dir, exist_ok=True)
        safe_name = "".join(c for c in restaurant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        html_file = f"{html_dir}/{safe_name}_{timestamp}.html"
        with open(html_file, 'w') as f:
            f.write(driver.page_source)
        
        # Helper function to get element by aria-label
        def get_by_aria_label(label):
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, f'[aria-label*="{label}"]')
                if elements:
                    text = elements[0].get_attribute("aria-label")
                    # If the label is at the start, remove it
                    if text.startswith(label):
                        return text[len(label):].strip()
                    return text.strip()
            except Exception as e:
                print(f"Error getting aria-label {label}: {str(e)}")
            return ""
            
        # Helper function to get elements by aria-label containing a string
        def get_all_by_aria_label(label):
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, f'[aria-label*="{label}"]')
                return [elem.get_attribute("aria-label").strip() for elem in elements if elem.get_attribute("aria-label")]
            except Exception as e:
                print(f"Error getting all aria-labels {label}: {str(e)}")
            return []
            
        # Helper function to clean category items
        def clean_category_items(items):
            cleaned = []
            for item in items:
                # Remove category labels if present
                for category in additional_info["categories"].keys():
                    if item.startswith(f"{category}: "):
                        item = item[len(f"{category}: "):]
                # Split by common separators and clean
                parts = [p.strip() for p in item.replace(" · ", "\n").split("\n")]
                cleaned.extend([p for p in parts if p and not p.startswith("http")])
            return list(set(cleaned))  # Remove duplicates
        
        # Get basic information
        for field, label in [
            ("address", "Address: "),
            ("phone", "Phone: "),
            ("website", "Website: "),
            ("menu", "Menu: "),
            ("price_range", "Price: ")
        ]:
            value = get_by_aria_label(label)
            if value:
                additional_info[field] = value
                print(f"Found {field}: {value}")
        
        # Get hours with better error handling
        try:
            hours_button = driver.find_element(By.CSS_SELECTOR, '[aria-label*="Hours"]')
            hours_button.click()
            time.sleep(2)  # Wait for hours to load
            
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day in days:
                hours = get_by_aria_label(f"{day}: ")
                if hours:
                    additional_info["hours"][day] = hours
                    print(f"Found hours for {day}: {hours}")
        except Exception as e:
            print(f"Error getting hours: {str(e)}")
        
        # Scroll to load all content
        panel_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div"
        scroll_panel_with_page_down(driver, panel_xpath, presses=5, pause_time=1)
        
        # Try to find and click the About section
        about_buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in about_buttons:
            try:
                if "About" in button.get_attribute("aria-label") or "About" in button.text:
                    button.click()
                    time.sleep(2)
                    break
            except:
                continue
        
        # Get all category information with better error handling
        for category in additional_info["categories"].keys():
            items = []
            # Try different variations of the category label
            variations = [
                f"{category}: ",
                category.lower() + ": ",
                category.title() + ": ",
                category.replace(" ", "") + ": "
            ]
            for label in variations:
                items.extend(get_all_by_aria_label(label))
            
            if items:
                additional_info["categories"][category] = clean_category_items(items)
                print(f"Found {category}: {additional_info['categories'][category]}")
        
        # Look for any unlabeled features
        all_features = driver.find_elements(By.CSS_SELECTOR, '.fontBodyMedium')
        feature_texts = []
        for elem in all_features:
            try:
                text = elem.text.strip()
                if text and len(text) > 3 and len(text) < 50:  # Reasonable length for a feature
                    feature_texts.append(text)
            except:
                continue
        
        # Clean and categorize features
        for text in feature_texts:
            # Skip if it's already in a category
            already_categorized = False
            for category_items in additional_info["categories"].values():
                if text in category_items:
                    already_categorized = True
                    break
            
            if not already_categorized:
                additional_info["features"].append(text)
        
        # Get about text with better filtering
        about_elements = driver.find_elements(By.CSS_SELECTOR, '.fontBodyMedium')
        for elem in about_elements:
            try:
                text = elem.text.strip()
                if len(text) > 50:  # Look for longer text that might be the description
                    # Check if it's not just a list of features
                    if not any(category in text for category in additional_info["categories"].keys()):
                        additional_info["about"] = text
                        print(f"Found about text: {text}")
                        break
            except:
                continue
        
        # Clean up features
        additional_info["features"] = list(set([
            f for f in additional_info["features"]
            if f and f != additional_info["address"]
            and f != additional_info["phone"]
            and f != additional_info["plus_code"]
            and not f.endswith(".com")
            and f not in ["Menu", "Your Maps activity"]
        ]))
        
    except Exception as e:
        print(f"Error extracting additional info: {str(e)}")
        traceback.print_exc()
    
    return additional_info

def main():
    # Create data directory if it doesn't exist
    os.makedirs('/opt/google-map-data/data/restaurant_pages', exist_ok=True)
    
    # Find the most recent restaurant JSON file
    results_dir = '/opt/google-map-data/Results'
    json_files = [f for f in os.listdir(results_dir) if f.startswith('restaurants_chattanooga_') and f.endswith('.json')]
    if not json_files:
        print("No restaurant data files found!")
        return
    
    latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(results_dir, x)))
    input_file = os.path.join(results_dir, latest_file)
    print(f"Reading from {input_file}")
    
    # Read the restaurant data
    with open(input_file, 'r') as f:
        restaurants = json.load(f)
    
    # Setup the driver
    driver = setup_driver()
    
    # Process the first 3 restaurants
    detailed_results = []
    for restaurant in restaurants[:3]:
        print(f"\nProcessing {restaurant['name']}...")
        
        # Get the basic info
        result = {
            "basic_info": restaurant,
            "additional_info": {}
        }
        
        # Get additional information
        result["additional_info"] = extract_additional_info(driver, restaurant["url"], restaurant["name"])
        detailed_results.append(result)
        
        # Save after each restaurant in case of errors
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'/opt/google-map-data/Results/detailed_restaurants_chattanooga_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(detailed_results, f, indent=2)
            
        print(f"Saved details for {restaurant['name']}")
        time.sleep(2)  # Be nice to Google's servers
    
    driver.quit()
    print("\nAll done! Check detailed_restaurants.json for results and the data/restaurant_pages directory for HTML files.")

if __name__ == "__main__":
    main()
