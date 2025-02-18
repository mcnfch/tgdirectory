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
        
        # Add additional options for stability
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--disable-notifications')
        
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                # Use webdriver-manager to handle driver installation
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=self.options)
                self.wait = WebDriverWait(self.driver, 20)
                print(f"WebDriver initialized successfully on attempt {attempt + 1}")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("Failed to initialize WebDriver after all attempts")
                    raise

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
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
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
                return
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("Failed to get location data after all attempts")
                    self.driver.save_screenshot(f"error_screenshot_{int(time.time())}.png")

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
    # Load cities from JSON file
    with open('/opt/noogabites/public/data/cities.json', 'r') as f:
        cities = json.load(f)

    # Add delay between processing each city
    city_delay = 30  # seconds
    
    for city in cities:
        try:
            print(f"\nProcessing {city['name']}, {city['state']}")
            driver = WebDriver()
            restaurants_data = []  # Initialize the list here
            
            # Process the city
            search_query = f"restaurants in {city['name']}, {city['state']}"
            maps_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            print(f"Opening URL...")
            driver.driver.get(maps_url)
            
            # Add delay after loading the page
            time.sleep(5)
            
            try:
                try:
                    accept_button = driver.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept all']"))
                    )
                    accept_button.click()
                except:
                    print("No accept button found")

                print("\nWaiting for sidebar to load...")
                sidebar = driver.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ecceSd"))
                )
                print("Found sidebar")
                
                # Initial result count
                initial_results = len(sidebar.find_elements(By.CSS_SELECTOR, "div.Nv2PK"))
                print(f"\nInitial result count: {initial_results}")
                
                # Scroll the sidebar to load more results
                try:
                    # Try different selectors for the results container
                    selectors = [
                        f"div[aria-label='Results for {search_query}']",
                        f"div[aria-label*='{search_query}']",
                        "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd",  # New selector
                        "div.m6QErb.DxyBCb.kA9KIf.dS8AEf"  # Alternative selector
                    ]
                    
                    results_div = None
                    for selector in selectors:
                        try:
                            results_div = driver.wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            print(f"Found results container with selector: {selector}")
                            break
                        except:
                            continue
                    
                    if not results_div:
                        raise Exception("Could not find results container with any selector")
                    
                    print("Found results container")
                    scroll_count = 0
                    last_count = 0
                    no_change_count = 0
                    keep_scrolling = True
                    
                    while keep_scrolling and scroll_count < 20:  # Limit to 20 scrolls
                        scroll_count += 1
                        print(f"\rScrolling... ({scroll_count})", end="", flush=True)
                        
                        # Scroll the results div
                        driver.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_div)
                        time.sleep(2)  # Increased delay
                        
                        # Get current results
                        current_results = len(results_div.find_elements(By.CSS_SELECTOR, "div.Nv2PK"))
                        
                        # Check if we've reached the end
                        if current_results == last_count:
                            no_change_count += 1
                            if no_change_count >= 3:  # If no change for 3 consecutive scrolls
                                print("\nNo more results loading")
                                keep_scrolling = False
                        else:
                            no_change_count = 0
                            
                        last_count = current_results
                        
                    print(f"\nTotal results after scrolling: {last_count}")
                    
                    if last_count == initial_results:
                        print("No additional results were loaded")
                    
                    # Save raw HTML data
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    raw_data_dir = os.path.join("/opt/noogabites/Results/crawl4ai")
                    os.makedirs(raw_data_dir, exist_ok=True)
                    
                    # Save full page HTML
                    full_page_html = driver.driver.page_source
                    html_file = os.path.join(raw_data_dir, f"full_page_{timestamp}.html")
                    with open(html_file, "w", encoding="utf-8") as f:
                        f.write(full_page_html)
                    print(f"\nSaved full page HTML to {html_file}")
                    
                    # Process results
                    results = results_div.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
                    total_results = len(results)
                    print("\nBeginning to process results...")
                    
                    for i, result in enumerate(results, 1):
                        print(f"\rProcessing restaurant {i}/{total_results}", end="", flush=True)
                        restaurant_data = {
                            "name": "",
                            "rating": "",
                            "reviews_count": "",
                            "price": "",
                            "cuisine": "",
                            "address": "",
                            "url": "",
                            "timestamp": timestamp
                        }
                        
                        try:
                            # Get name
                            try:
                                name_element = result.find_element(By.CSS_SELECTOR, "div.qBF1Pd.fontHeadlineSmall")
                                restaurant_data["name"] = name_element.text.strip()
                            except:
                                print(f"\nError getting name for restaurant {i}")
                            
                            # Get rating and reviews
                            try:
                                rating_element = result.find_element(By.CSS_SELECTOR, "span.MW4etd")
                                restaurant_data["rating"] = rating_element.text.strip()
                                
                                reviews_element = result.find_element(By.CSS_SELECTOR, "span.UY7F9")
                                reviews_text = reviews_element.text.strip("()")
                                restaurant_data["reviews_count"] = reviews_text
                            except:
                                print(f"\nError getting rating/reviews for restaurant {i}")
                            
                            # Get price and cuisine
                            try:
                                details_element = result.find_element(By.CSS_SELECTOR, "div.UaQhfb.fontBodyMedium")
                                details_text = details_element.text
                                if "·" in details_text:
                                    parts = details_text.split("·")
                                    restaurant_data["price"] = parts[0].strip()
                                    restaurant_data["cuisine"] = parts[1].strip() if len(parts) > 1 else ""
                            except:
                                print(f"\nError getting price/cuisine for restaurant {i}")
                            
                            # Get address
                            try:
                                address_element = result.find_element(By.CSS_SELECTOR, "div.W4Efsd:last-child > div.W4Efsd:last-child > span.W4Efsd:last-child")
                                restaurant_data["address"] = address_element.text.strip()
                            except:
                                print(f"\nError getting address for restaurant {i}")
                            
                            # Get URL
                            try:
                                url_element = result.find_element(By.CSS_SELECTOR, "a.hfpxzc")
                                restaurant_data["url"] = url_element.get_attribute("href")
                            except:
                                print(f"\nError getting URL for restaurant {i}")
                            
                            restaurants_data.append(restaurant_data)
                            
                        except Exception as e:
                            print(f"\nError processing restaurant {i}: {str(e)}")
                    
                    print("\n\nAll restaurants processed")
                    
                    # Save results to file
                    print("\nSaving results to file...")
                    results_file = os.path.join(raw_data_dir, f"restaurants_{city['name']}_{timestamp}.json")
                    with open(results_file, "w", encoding="utf-8") as f:
                        json.dump(restaurants_data, f, indent=2, ensure_ascii=False)
                    print(f"Results saved to {results_file}")
                    
                except Exception as e:
                    print(f"Error finding results: {str(e)}")
            
            except Exception as e:
                print(f"Error processing {city['name']}: {str(e)}")
            
        except Exception as e:
            print(f"Error processing {city['name']}: {str(e)}")
        finally:
            try:
                driver.driver.quit()
            except:
                pass
            
            print(f"Waiting {city_delay} seconds before processing next city...")
            time.sleep(city_delay)