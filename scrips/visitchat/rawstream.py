#!/usr/bin/env python3
import asyncio
from datetime import datetime
import json
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class RawStreamMonitor:
    def __init__(self):
        self.base_url = "https://www.visitchattanooga.com/restaurants/"
        self.stream_file = None
        
        # Configure browser with performance logging
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL", "browser": "ALL"}
        
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--enable-javascript')
        
        self.driver = uc.Chrome(options=options, desired_capabilities=capabilities)

    def wait_for_ajax(self, timeout=10):
        """Wait for jQuery AJAX calls to complete"""
        script = """
        return (typeof jQuery !== 'undefined') ? jQuery.active : 0;
        """
        start_time = time.time()
        while time.time() < start_time + timeout:
            ajax_count = self.driver.execute_script(script)
            if ajax_count == 0:
                return True
            time.sleep(0.5)
        raise TimeoutException("Timeout waiting for AJAX calls to complete")

    def wait_for_network_idle(self, timeout=10):
        """Wait for network to become idle"""
        script = """
        return window.performance.getEntriesByType('resource').length;
        """
        previous_count = self.driver.execute_script(script)
        start_time = time.time()
        while time.time() < start_time + timeout:
            current_count = self.driver.execute_script(script)
            if current_count == previous_count:
                return True
            previous_count = current_count
            time.sleep(0.5)
        return False

    def _open_stream_file(self):
        results_dir = "/opt/noogabites/Results/visitchat"
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stream_path = f"{results_dir}/raw_stream_{timestamp}.txt"
        self.stream_file = open(stream_path, 'w')
        print(f"Saving raw stream to: {stream_path}")
        return stream_path

    def process_browser_logs_for_network_events(self, logs):
        """Process logs and yield network-related events"""
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if ("Network.response" in log["method"] or 
                "Network.request" in log["method"] or 
                "Network.webSocket" in log["method"]):
                yield log

    async def monitor_network(self):
        """Capture and save network traffic"""
        stream_path = self._open_stream_file()

        print("Loading page...")
        self.driver.get(self.base_url)
        
        # Wait for initial page load
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        print("Page loaded, waiting for dynamic content...")

        # Scroll multiple times to trigger all lazy loading
        for i in range(3):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            print(f"Scroll {i+1}/3...")
            await asyncio.sleep(2)
            
            try:
                self.wait_for_ajax()
                self.wait_for_network_idle()
            except TimeoutException as e:
                print(f"Warning: {str(e)}")

        print("Capturing network traffic...")

        # Get all logs
        perf_logs = self.driver.get_log("performance")
        browser_logs = self.driver.get_log("browser")
        
        # Process and write performance logs
        events = self.process_browser_logs_for_network_events(perf_logs)
        for event in events:
            self.stream_file.write("\n=== NEW PERFORMANCE EVENT ===\n")
            self.stream_file.write(json.dumps(event, indent=2))
            self.stream_file.write("\n")

        # Write browser logs
        for log in browser_logs:
            self.stream_file.write("\n=== NEW BROWSER LOG ===\n")
            self.stream_file.write(json.dumps(log, indent=2))
            self.stream_file.write("\n")

        self.stream_file.flush()
        print(f"Captured {len(perf_logs)} performance log entries")
        print(f"Captured {len(browser_logs)} browser log entries")
        
        # Keep monitoring for new traffic
        while True:
            await asyncio.sleep(2)
            new_perf_logs = self.driver.get_log("performance")
            new_browser_logs = self.driver.get_log("browser")
            
            if new_perf_logs or new_browser_logs:
                if new_perf_logs:
                    events = self.process_browser_logs_for_network_events(new_perf_logs)
                    for event in events:
                        self.stream_file.write("\n=== NEW PERFORMANCE EVENT ===\n")
                        self.stream_file.write(json.dumps(event, indent=2))
                        self.stream_file.write("\n")
                
                if new_browser_logs:
                    for log in new_browser_logs:
                        self.stream_file.write("\n=== NEW BROWSER LOG ===\n")
                        self.stream_file.write(json.dumps(log, indent=2))
                        self.stream_file.write("\n")
                
                self.stream_file.flush()

    async def run(self, duration=60):
        """Run stream capture"""
        monitor_task = asyncio.create_task(self.monitor_network())
        
        try:
            await asyncio.sleep(duration)
        finally:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
            if self.stream_file:
                self.stream_file.close()
            self.driver.quit()
            print("\nStream capture complete")

async def main():
    monitor = RawStreamMonitor()
    await monitor.run(duration=60)

if __name__ == "__main__":
    asyncio.run(main())
