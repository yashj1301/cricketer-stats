import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class Cricketer_Stats_Scraper:

    def __init__(self, player_name):
        self.player_name = player_name
        self.player_id = None
        self.player_url = None
    
        # Initialize class variables for storing stats
        self.battingstats = None
        self.bowlingstats = None
        self.allroundstats = None
        self.fieldingstats = None
        self.player_info = None

        # Set up the WebDriver and open the search URL
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        print("Setting up WebDriver...")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Call get_player_url() to fetch the player's URL and ID when the object is initialized
        self.get_player_url()

    def get_player_url(self):
        start_time = time.time()
        print(f"Extracting {self.player_name}'s player URL and Player ID....")
        search_url = f"https://search.espncricinfo.com/ci/content/site/search.html?search={self.player_name.lower().replace(' ', '%20')};type=player"
        

        try:

            # Open the search URL
            self.driver.get(search_url)

            # Extract the player ID and URL from the search results
            player_link_element = self.driver.find_element(By.CSS_SELECTOR, "h3.name.link-cta a")
            self.player_url = player_link_element.get_attribute("href")
            self.player_id = self.player_url.split('-')[-1]
            
            # record the time taken
            print(f"Extraction Successful for {self.player_name}.")
            end_time = time.time()
            print(f"Time taken to extract URL: {end_time - start_time:.2f} seconds")
        
        except Exception as e:
            
            print(f"Error in extracting {self.player_name}'s url:", e)
            return None, None

    def extract_inns_data(self, record_type):
        start_time = time.time()
        print(f"Starting extraction of {self.player_name}'s {record_type} stats....")
        
        # Construct the search URL based on record_type (batting, bowling, etc.)
        search_url = f"https://stats.espncricinfo.com/ci/engine/player/{self.player_id}.html?class=11;template=results;type={record_type};view=innings"
        
        # Open the URL
        self.driver.get(search_url)

        # Step 1: Extract the headers of the table
        headers = self.driver.find_elements(By.CSS_SELECTOR, "thead tr.headlinks th")
        header_names = [header.text for header in headers if header.text != ''] + ['Match id']  # Add match_id column name
        
        # Step 2: Extract the data from the 4th tbody
        rows = self.driver.find_elements(By.XPATH, "(//tbody)[4]//tr")
        
        # Step 3: Extract the data column-wise and store it in a list
        player_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells if cell.text != '']
            player_data.append(row_data)
        
        # Step 4: Create a DataFrame from the extracted data
        innings_data = pd.DataFrame(player_data, columns=header_names)
        
        end_time = time.time()
        print(f"Extracted {innings_data.shape[0]} records in {end_time - start_time:.2f} seconds")
        
        return innings_data

    def extract_player_info(self):
        try:
            start_time = time.time()
            print(f"Starting extraction of {self.player_name}'s personal info....")
            
            # Start by opening the player info URL
            search_url = f"https://www.espncricinfo.com/cricketers/{self.player_name.replace(' ', '-').lower()}-{self.player_id}"
            self.driver.get(search_url)

            # Step 1: Extract headers within the specified div tag
            headers = self.driver.find_elements(By.XPATH, "//div[@class='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8']//p[@class='ds-text-tight-m ds-font-regular ds-uppercase ds-text-typo-mid3']")
            header_names = [header.text for header in headers]

            # Step 2: Extract values within the specified div tag
            values = self.driver.find_elements(By.XPATH, "//div[@class='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8']//span[@class='ds-text-title-s ds-font-bold ds-text-typo']")
            value_texts = [value.text for value in values]

            # Step 3: Create a DataFrame from the extracted data
            player_info = pd.DataFrame([value_texts], columns=header_names)

            end_time = time.time()
            print(f"Extracted player info in {end_time - start_time:.2f} seconds")

            return player_info
            
        except Exception as e:
            print(f"Error in extracting {self.player_name}'s personal info:", e)
            return None

    def get_player_stats(self, stats_type="all"):
        try:
            # Ensure that player_id is available
            if not self.player_id:
                print("Player ID is not available. Run get_player_url() first.")
                return
            
            # Fetch personal information if 'personalinfo' is passed
            if stats_type == "personal_info":
                self.player_info = self.extract_player_info()
            
            # Fetch batting stats if 'all' or 'batting' is passed
            if stats_type == "all" or stats_type == "batting":
                self.battingstats = self.extract_inns_data('batting')

            # Fetch bowling stats if 'all' or 'bowling' is passed
            if stats_type == "all" or stats_type == "bowling":
                self.bowlingstats = self.extract_inns_data('bowling')

            # Check if the player is an all-rounder and fetch all-round stats
            if stats_type == "all" or stats_type == "allround":
                self.player_info = self.extract_player_info()
                if self.player_info is not None and 'allround' in self.player_info['PLAYING ROLE'][0].lower():
                    self.allroundstats = self.extract_inns_data('allround')

            # Fetch fielding stats if 'all' or 'fielding' is passed
            if stats_type == "all" or stats_type == "fielding":
                self.fieldingstats = self.extract_inns_data('fielding')        

        except Exception as e:
            print(f"Error in extracting stats for {self.player_name}: ", e)


    def __del__(self):
        try:
            self.driver.quit()
            print("WebDriver closed successfully.")
        except Exception as e:
            print("Error while closing the WebDriver:", e)

