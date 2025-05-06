## Documentation for `scraper.py`

### Overview

The `scraper.py` module defines the **`ScrapeData`** class (alias for `Cricketer_Stats_Scraper`), which automates extraction of a player’s statistics and personal info from ESPN CricInfo using Selenium.

---

### Requirements

- **time** (standard library)  
- **pandas**  
- **selenium**  
- **undetected_chromedriver**  

Make sure to have a compatible ChromeDriver installed or let `webdriver_manager` install it automatically.

---

### Class Definition

```python
class ScrapeData:
    def __init__(self, player_name: str): ...
    def get_player_url(self) -> None: ...
    def extract_inns_data(self, record_type: str) -> pd.DataFrame: ...
    def extract_player_info(self) -> pd.DataFrame: ...
    def get_player_stats(self, stats_type: str = "all") -> None: ...
    def __del__(self) -> None: ...
```

#### 1. Constructor

```python
def __init__(self, player_name: str):
    """
    Initializes the ScrapeData object.
    - Stores `player_name`.
    - Launches a Chrome WebDriver.
    - Automatically calls `get_player_url()` to populate:
        - self.player_url
        - self.player_id
    """
```
__Parameters__

`player_name` (str): Full name of the cricketer to scrape.

__Result__

calls `get_player_url()` to fetch player id and player url as soon as object is created. 


#### 2. `get_player_url(self)`

```python
def get_player_url(self) -> None:
    """
    Searches ESPN CricInfo for `self.player_name`,
    extracts the first matching profile URL and player ID.
    
    Updates:
      - self.player_url (str)
      - self.player_id  (str)
    """
```

It extracts the __player url__ and __player id__ from the website, and stores to instance variables. 

#### 3. `extract_inns_data(self, record_type)`

```python
def extract_inns_data(self, record_type: str) -> pd.DataFrame:
    """
    Scrapes innings-level stats for the given `record_type`.
    
    Args:
      record_type (str): One of "batting", "bowling", "fielding", "allround".
    
    Returns:
      pd.DataFrame: Tabular stats for each innings, with columns like "Runs", "Overs", etc.
    """
```

1. Builds the URL for the desired stats view.
2. Parses table headers and rows via Selenium.
3. Returns a DataFrame with a final “Match ID” column.

#### 4. `extract_player_info(self)`

```python
def extract_player_info(self) -> pd.DataFrame:
    """
    Visits the player profile page (`self.player_url`) and extracts
    personal details (name, country, age, playing role).
    
    Returns:
      pd.DataFrame: Single-row DataFrame with columns "Player ID", "Player URL", plus other personal info fields.
    """
```

Returns DataFrame of personal info for the player (or None on failure).

#### 5. `get_player_stats(self, stats_type="all")`

```python
def get_player_stats(self, stats_type: str = "all") -> None:
    """
    Orchestrates the full scraping process.
    
    Args:
      stats_type (str):  
        - "batting", "bowling", "fielding", "allround", "personal_info", or "all" (default).
    
    Behavior:
      - Calls `extract_player_info()` if needed.
      - Calls `extract_inns_data()` for each requested stat.
      - Exports each DataFrame to CSV if `export=True`.
    
    Updates:
      - self.battingstats, self.bowlingstats, self.fieldingstats,
        self.allroundstats, self.player_info
    """
```

This is the high-level method used in the driver functions to put everything in motion. After the object is created, the data scraping command is given through this method and its `stat_type` argument. 

#### 6. Destructor

```python
def __del__(self) -> None:
    """
    Destructor: ensures the Selenium WebDriver is cleanly closed
    when the scraper object is garbage-collected.
    """
```

This prevents orphaned ChromeDriver processes by calling `self.driver.quit()`.

### Usage Example

```python
from scripts.scraper.scraper import ScrapeData

# 1. Initialize and fetch URL, player ID
scraper = ScrapeData("Virat Kohli")

# 2. Scrape all stats (batting, bowling, fielding, allround, personal info)
scraper.get_player_stats("all")

# 3. Access the DataFrames
print(scraper.battingstats.head())
print(scraper.bowlingstats.head())
print(scraper.player_info)
```







