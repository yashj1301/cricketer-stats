## Documentation for `scraper.py`

### Overview
The `scraper.py` script is designed to scrape cricket player statistics from ESPN CricInfo. It extracts the player's batting, bowling, all-rounder, and fielding stats along with personal information such as the player's country, age, and playing role. This script uses **Selenium** for web scraping, running in _headless mode_ for efficiency.

### Features
- Scrapes player statistics for batting, bowling, all-round performance, and fielding.
- Extracts personal information about the player like full name, age, country, and playing role.
- Uses Selenium WebDriver in headless mode for silent and efficient web scraping.

## Requirements
- Python 3.x
- Libraries:
  - `selenium`
  - `webdriver-manager`
  - `pandas`
- Google Chrome installed with the corresponding version of Chromedriver.

The libraries can also be found in the `requirements.txt` file in the root project folder. 
  
Install the required libraries using pip:
        
        pip install selenium webdriver-manager pandas

### Usage
1. Initialize the `Cricketer_Stats_Scraper` class with the player's name.
2. Fetch the desired stats by calling `get_player_stats()`.
3. Access the scraped data in the `battingstats`, `bowlingstats`, `allroundstats`, `fieldingstats`, and player_info variables.

#### Example usage

    from scraper import Cricketer_Stats_Scraper

#### Initialize the scraper for a specific player
    scraper = Cricketer_Stats_Scraper("Virat Kohli")

#### Fetch all stats (batting, bowling, fielding, all-round)
    scraper.get_player_stats(stats_type="all")

#### Print the fetched data
    print("Batting Stats:", scraper.battingstats)
    print("Bowling Stats:", scraper.bowlingstats)
    print("Allround Stats:", scraper.allroundstats)
    print("Fielding Stats:", scraper.fieldingstats)

#### Access personal player info
    print("Player Info:", scraper.player_info)

### Methods

1. __`__init__(self,player_name)`__

__Description__: Initializes the `Cricketer_Stats_Scraper` object with the player's name. Sets up the WebDriver, and automatically calls `get_player_url()` to fetch the player's URL and ID.

__Parameters__:
- `player_name (str)`: The name of the cricketer whose stats will be scraped.

__Returns__: None; updates the instance variables `player_id` and `player_url`. 

2. __`get_player_url()`__

__Description__: Extracts the player URL and player ID by searching the player's name on ESPN CricInfo.

__Returns__: None, updates the `player_url` and `player_id` instance variables.

3. __`extract_inns_data(record_type)`__

__Description__: Scrapes innings data (batting, bowling, fielding, or all-round stats) for the player based on the provided record_type.

__Parameters__: 
- `record_type (str)` - Type of stats to scrape ("batting","bowling","fielding", "allround").

__Returns__: A pandas DataFrame containing the player's innings data, based on record type.

4. __`extract_player_info()`__

__Description__: Extracts the personal information of the player (full name, country, age, and playing role).

__Returns__: A pandas DataFrame containing the player's personal information.

5. __`get_player_stats(stats_type="all")`__

___Description__: Fetches stats based on the stats_type argument.

__Parameters__: 
- `stats_type (str)` - Stats to fetch. Can be "batting", "bowling", "allround", "fielding", or "all" to fetch all stats (default).

__Returns__: None; updates the instance variables `battingstats`, `bowlingstats`, `allroundstats`, `fieldingstats`, and `player_info`.

6.__` __del__()`__

__Description__: Destructor of the class. It cleans up the WebDriver instance after the scraping process is complete by closing the browser window.