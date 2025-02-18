from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

class WebDriver:
    def __init__(self):
        self.location_data = {
            "rating": "NA",
            "reviews_count": "NA",
            "location": "NA",
            "contact": "NA",
            "website": "NA",
            "Time": {day: "NA" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            "Reviews": [],
            "Popular Times": {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        }
        
        self.options = Options()
        self.options.add_argument('--headless=new')  # new headless mode
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36')
        
        # Use webdriver-manager to handle driver installation
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.wait = WebDriverWait(self.driver, 20)

    def click_open_close_time(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "section-info-hour-text")
            ))
            ActionChains(self.driver).move_to_element(element).click().perform()
        except:
            pass

    def click_all_reviews_button(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "allxGeDnJMl__button")
            ))
            element.click()
            return True
        except:
            return False

    def get_location_data(self):
        try:
            # Wait for and find elements
            avg_rating = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.ceNzKf")
            ))
            total_reviews = self.driver.find_element(By.CSS_SELECTOR, "button[jsaction='pane.rating.moreReviews']")
            address = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']")
            phone_number = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id^='phone']")
            website = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
            
            # Store the data
            self.location_data["rating"] = avg_rating.text
            self.location_data["reviews_count"] = total_reviews.text.split()[0]
            self.location_data["location"] = address.text
            self.location_data["contact"] = phone_number.text
            self.location_data["website"] = website.text
        except Exception as e:
            print(f"Error getting location data: {str(e)}")

    def get_location_open_close_time(self):
        try:
            days = self.driver.find_elements(By.CLASS_NAME, "lo7U087hsMA__row-header")
            times = self.driver.find_elements(By.CLASS_NAME, "lo7U087hsMA__row-interval")
            
            for day, time in zip(days, times):
                self.location_data["Time"][day.text] = time.text
        except Exception as e:
            print(f"Error getting hours: {str(e)}")

    def get_popular_times(self):
        try:
            graphs = self.driver.find_elements(By.CLASS_NAME, "section-popular-times-graph")
            days = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 
                   4: "Thursday", 5: "Friday", 6: "Saturday"}
            
            for idx, graph in enumerate(graphs):
                bars = graph.find_elements(By.CLASS_NAME, "section-popular-times-bar")
                times = [bar.get_attribute("aria-label") for bar in bars]
                self.location_data["Popular Times"][days[idx]] = times
        except Exception as e:
            print(f"Error getting popular times: {str(e)}")

    def scroll_the_page(self):
        try:
            scrollable_div = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.section-layout.section-scrollbox.scrollable-y")
            ))
            
            for _ in range(5):  # Scroll 5 times
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', 
                    scrollable_div
                )
                time.sleep(2)
        except Exception as e:
            print(f"Error scrolling: {str(e)}")

    def expand_all_reviews(self):
        try:
            more_buttons = self.driver.find_elements(By.CLASS_NAME, "section-expand-review")
            for button in more_buttons:
                button.click()
                time.sleep(0.1)
        except Exception as e:
            print(f"Error expanding reviews: {str(e)}")

    def get_reviews_data(self):
        try:
            review_items = self.driver.find_elements(By.CSS_SELECTOR, "div.section-review")
            
            for item in review_items:
                try:
                    name = item.find_element(By.CLASS_NAME, "section-review-title").text
                    text = item.find_element(By.CLASS_NAME, "section-review-review-content").text
                    date = item.find_element(By.CLASS_NAME, "section-review-publish-date").text
                    stars = item.find_element(By.CLASS_NAME, "section-review-stars").get_attribute("aria-label")
                    
                    self.location_data["Reviews"].append({
                        "name": name,
                        "review": text,
                        "date": date,
                        "rating": stars
                    })
                except:
                    continue
        except Exception as e:
            print(f"Error getting reviews: {str(e)}")

    def scrape(self, url):
        try:
            self.driver.get(url)
            time.sleep(5)  # Wait for initial load
            
            # Get basic location data
            self.get_location_data()
            
            # Get hours
            self.click_open_close_time()
            time.sleep(2)
            self.get_location_open_close_time()
            
            # Get popular times
            self.get_popular_times()
            
            # Get reviews
            if self.click_all_reviews_button():
                time.sleep(3)
                self.scroll_the_page()
                self.expand_all_reviews()
                self.get_reviews_data()
            
            return self.location_data
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return None
        finally:
            self.driver.quit()

if __name__ == "__main__":
    URL = "https://www.google.com/maps/search/restaurants+in+Chattanooga,+TN/@34.9923527,-85.2398322,10.53z/data=!4m2!2m1!6e5?entry=ttu&g_ep=EgoyMDI1MDIwNS4xIKXMDSoASAFQAw%3D%3D"
    scraper = WebDriver()
    results_dir = "/opt/google-map-data/Results"
    restaurants_data = []
    
    try:
        print("Opening URL...")
        scraper.driver.get(URL)
        time.sleep(10)
        
        try:
            try:
                accept_button = scraper.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept all']"))
                )
                accept_button.click()
                print("Clicked accept button")
            except:
                print("No accept button found")

            print("\nWaiting for sidebar to load...")
            sidebar = scraper.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ecceSd"))
            )
            print("Found sidebar")
            
            # Function to scroll the sidebar
            def scroll_sidebar():
                try:
                    print("\nStarting scroll process...")
                    
                    # Find the results container using the query-specific aria-label
                    query = "restaurants in Chattanooga"
                    try:
                        # Try exact match first
                        results_div = scraper.driver.find_element(By.CSS_SELECTOR, f"div[aria-label='Results for {query}']")
                    except:
                        # Try partial match if exact fails
                        results_div = scraper.driver.find_element(By.CSS_SELECTOR, f"div[aria-label*='{query}']")
                    
                    print("Found results container")
                    scroll_count = 0
                    start_time = time.time()
                    last_count = 0
                    same_count_iterations = 0
                    
                    keep_scrolling = True
                    while keep_scrolling and scroll_count < 50:  # Limit to 50 attempts
                        scroll_count += 1
                        print(f"\nScroll attempt #{scroll_count}...")
                        
                        # Send PAGE_DOWN key twice with a small delay
                        results_div.send_keys(Keys.PAGE_DOWN)
                        time.sleep(0.5)
                        results_div.send_keys(Keys.PAGE_DOWN)
                        time.sleep(0.5)
                        
                        # Check if we've reached the end
                        page_source = scraper.driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
                        if "You've reached the end of the list." in page_source:
                            print("Reached end of list!")
                            keep_scrolling = False
                            break
                            
                        # Get current number of results
                        current_results = len(sidebar.find_elements(By.CSS_SELECTOR, "div.Nv2PK"))
                        elapsed_time = int(time.time() - start_time)
                        print(f"Current results: {current_results} (after {elapsed_time} seconds)")
                        
                        # Check if we're still getting new results
                        if current_results == last_count:
                            same_count_iterations += 1
                            if same_count_iterations >= 5:  # If no new results after 5 attempts, stop
                                print(f"\nNo new results after {same_count_iterations} attempts, stopping...")
                                break
                        else:
                            same_count_iterations = 0
                            print(f"Found {current_results - last_count} new results")
                            
                        last_count = current_results
                        
                        # Alternative approach: try to scroll the last result into view
                        try:
                            all_results = scraper.driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
                            if all_results:
                                last_result = all_results[-1]
                                scraper.driver.execute_script("arguments[0].scrollIntoView(true);", last_result)
                        except Exception as e:
                            print(f"Error during scrollIntoView: {str(e)}")
                        
                        # Wait a bit longer to ensure results load
                        time.sleep(2)
                        
                except Exception as e:
                    print(f"Error during scrolling: {str(e)}")
                    import traceback
                    print(traceback.format_exc())
            
            # Initial result count
            initial_results = len(sidebar.find_elements(By.CSS_SELECTOR, "div.Nv2PK"))
            print(f"\nInitial result count: {initial_results}")
            
            # Scroll to load all results
            print("\nStarting scroll process to load more results...")
            scroll_sidebar()
            
            # Get all results after scrolling
            results = sidebar.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
            total_results = len(results)
            print(f"\nTotal results after scrolling: {total_results}")
            
            if total_results > initial_results:
                print(f"Successfully loaded {total_results - initial_results} additional results")
            else:
                print("No additional results were loaded")
            
            # Save raw HTML data for analysis
            try:
                raw_data_dir = "/opt/google-map-data/data"
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save full page HTML
                full_page_html = scraper.driver.page_source
                with open(f"{raw_data_dir}/full_page_{timestamp}.html", "w", encoding="utf-8") as f:
                    f.write(full_page_html)
                print(f"\nSaved full page HTML to {raw_data_dir}/full_page_{timestamp}.html")
                
                # Save individual restaurant elements
                results = sidebar.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
                for i, result in enumerate(results, 1):
                    restaurant_html = result.get_attribute('outerHTML')
                    with open(f"{raw_data_dir}/restaurant_{i}_{timestamp}.html", "w", encoding="utf-8") as f:
                        f.write(restaurant_html)
                print(f"Saved {len(results)} individual restaurant HTML files")
            except Exception as e:
                print(f"Error saving raw HTML: {str(e)}")
            
            print("\nBeginning to process results...")
            for i, result in enumerate(results, 1):
                print(f"\rProcessing restaurant {i}/{total_results}", end="", flush=True)
                restaurant_data = {
                    "name": "",
                    "rating": "",
                    "reviews": "",
                    "price": "",
                    "category": "",
                    "address": "",
                    "description": "",
                    "hours": "",
                    "url": "",
                    "scrape_time": datetime.now().isoformat()
                }
                
                try:
                    # Get URL
                    try:
                        url_element = result.find_element(By.CSS_SELECTOR, "a.hfpxzc")
                        restaurant_data["url"] = url_element.get_attribute("href")
                    except:
                        pass
                    
                    # Name
                    restaurant_data["name"] = result.find_element(By.CSS_SELECTOR, "div.qBF1Pd").text
                    
                    # Rating and reviews
                    try:
                        rating_element = result.find_element(By.CSS_SELECTOR, "span.MW4etd")
                        reviews_element = result.find_element(By.CSS_SELECTOR, "span.UY7F9")
                        restaurant_data["rating"] = rating_element.text
                        restaurant_data["reviews"] = reviews_element.text.strip('()')
                    except:
                        pass

                    # Get all info sections
                    info_sections = result.find_elements(By.CSS_SELECTOR, "div.W4Efsd")

                    # Category/Cuisine type
                    restaurant_data["category"] = "Not listed"  # Default value
                    try:
                        # Look for the category in the nested W4Efsd divs
                        for div in info_sections:
                            nested_divs = div.find_elements(By.CSS_SELECTOR, "div.W4Efsd")
                            for nested_div in nested_divs:
                                spans = nested_div.find_elements(By.CSS_SELECTOR, "span")
                                if len(spans) >= 1:  # First span in the nested div contains the category
                                    category_text = spans[0].text.strip()
                                    if category_text and not any(char in category_text for char in '$1234567890()·'):
                                        restaurant_data["category"] = category_text
                                        break
                            if restaurant_data["category"] != "Not listed":
                                break
                    except Exception as e:
                        print(f"Error getting category: {str(e)}")
                    
                    # Price range
                    try:
                        if info_sections:
                            info_text = info_sections[0].text
                            if '·' in info_text:
                                parts = info_text.split('·')
                                for part in parts:
                                    part = part.strip()
                                    if '$' in part:
                                        restaurant_data["price"] = part
                    except:
                        pass
                    
                    # Process remaining sections
                    for section in info_sections[1:]:
                        text = section.text
                        
                        # Skip if empty
                        if not text:
                            continue
                            
                        # If contains address pattern (numbers and street)
                        if any(char.isdigit() for char in text) and any(word in text.lower() for word in ['st', 'ave', 'rd', 'blvd']):
                            if '·' in text:
                                parts = text.split('·')
                                for part in parts:
                                    if any(char.isdigit() for char in part) and any(word in part.lower() for word in ['st', 'ave', 'rd', 'blvd']):
                                        restaurant_data["address"] = part.strip()
                                        break
                            else:
                                restaurant_data["address"] = text
                                
                        # If contains hours pattern
                        elif any(word in text.lower() for word in ['open', 'closed', 'reopens']):
                            restaurant_data["hours"] = text
                            
                        # If looks like a description (doesn't contain hours or address patterns)
                        elif not restaurant_data["description"] and not any(word in text.lower() for word in ['open', 'closed', 'reopens']) and not any(char.isdigit() for char in text):
                            restaurant_data["description"] = text
                            
                    restaurants_data.append(restaurant_data)
                    
                except Exception as e:
                    print(f"\nError processing restaurant {i}: {str(e)}")
            
            print("\n\nAll restaurants processed")
            
            # Save results to file
            print("\nSaving results to file...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(results_dir, f"restaurants_chattanooga_{timestamp}.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(restaurants_data, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully saved {len(restaurants_data)} restaurant records to {output_file}")
                
        except Exception as e:
            print(f"Error finding results: {str(e)}")
            
    except Exception as e:
        print(f"Error getting location data: {str(e)}")
    finally:
        scraper.driver.quit()