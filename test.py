from scripts.scraper.scraper import Cricketer_Stats_Scraper as PlayerStatsScraper
import pandas as pd

# Example usage:
player_name = "Virat Kohli"
player = PlayerStatsScraper(player_name)

#Get player stats (batting, bowling, and check for allrounder stats)
player.get_player_stats()

if player.allroundstats is not None:
    print(f"{player_name} is an all-rounder. Here are the stats:")
    pd.to_csv(player.allroundstats, "/data/player_allrounder_stats.csv")
else:
    print(f"{player_name} is not an all-rounder.")


# export the player's personal info
player.player_info.to_csv("data/player_personal_info.csv", index=False)
print(f"Player personal info exported to data/player_personal_info.csv")

player.battingstats.to_csv("data/player_batting_stats.csv", index=False)
print(f"Player batting stats exported to data/player_batting_stats.csv")

player.bowlingstats.to_csv("data/player_bowling_stats.csv", index=False)
print(f"Player bowling stats exported to data/player_bowling_stats.csv")

player.fieldingstats.to_csv("data/player_fielding_stats.csv", index=False)
print(f"Player fielding stats exported to data/player_fielding_stats.csv")


