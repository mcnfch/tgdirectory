from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import sys
from datetime import datetime

class GoogleMapsScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920,1080')
        self.options.set_preference('intl.accept_languages', 'en-US, en')
        self.options.set_preference('dom.webdriver.enabled', False)
        
        service = Service('/usr/local/bin/geckodriver')
        self.driver = webdriver.Firefox(service=service, options=self.options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def scrape_url(self, url):
        """Scrape data from the given Google Maps URL"""
        try:
            self.driver.get(url)
            time.sleep(5)  # Initial wait for page load
            
            # Wait for results to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="article"]')))
            
            # Scroll to load more results
            self._scroll_results()
            
            # Extract data
            results = []
            items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
            
            for item in items[:20]:  # Limit to first 20 results for testing
                try:
                    # Click on the item to load details
                    item.click()
                    time.sleep(2)
                    
                    # Wait for details to load
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf')))
                    
                    data = {
                        'name': self._safe_get_text('h1.DUwDvf'),
                        'rating': self._safe_get_text('span.ceNzKf'),
                        'reviews': self._safe_get_text('button[jsaction="pane.rating.moreReviews"]'),
                        'address': self._safe_get_text('button[data-item-id="address"]'),
                        'website': self._safe_get_text('a[data-item-id="authority"]'),
                        'phone': self._safe_get_text('button[data-item-id^="phone"]'),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    results.append(data)
                    print(f"Scraped: {data['name']}")
                    
                except Exception as e:
                    print(f"Error processing item: {str(e)}")
                    continue
            
            # Save results
            self._save_results(results)
            return results
            
        except Exception as e:
            print(f"Error scraping URL: {str(e)}")
            return None
        finally:
            self.close()
    
    def _scroll_results(self, max_scrolls=10):
        """Scroll through results to load more items"""
        scrolls = 0
        while scrolls < max_scrolls:
            try:
                # Scroll the results panel
                self.driver.execute_script(
                    'document.querySelector(\'div[role="feed"]\').scrollTop += 1000'
                )
                time.sleep(2)
                scrolls += 1
            except Exception:
                break
    
    def _safe_get_text(self, selector):
        """Safely extract text from an element"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except:
            return ''
    
    def _save_results(self, results):
        """Save results to a JSON file"""
        if results:
            filename = f'results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Results saved to {filename}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 maps_scraper.py <google_maps_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    scraper = GoogleMapsScraper()
    try:
        results = scraper.scrape_url(url)
        if results:
            print(f"Successfully scraped {len(results)} locations")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
