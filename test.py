from scripts.scraper.scraper import Cricketer_Stats_Scraper as PlayerStatsScraper
import pandas as pd

# Example usage:
player_name = "Virat Kohli"
player = PlayerStatsScraper(player_name)

#Get player stats (batting, bowling, and check for allrounder stats)
player.get_player_stats("personal_info",export=False)

