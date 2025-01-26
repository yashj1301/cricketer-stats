from scripts.scraper.scraper import Cricketer_Stats_Scraper as PlayerStatsScraper

# Example usage:
player_name = "Hardik Pandya"
player = PlayerStatsScraper(player_name)

#Get player stats (batting, bowling, and check for allrounder stats)
player.get_player_stats()

# Print the player's batting stats
print(player.battingstats)

# Print the player's bowling stats
print(player.bowlingstats)

# Print the player's fielding stats
print(player.fieldingstats)

if player.allroundstats is not None:
    print(player.allroundstats)
else:
    print(f"{player_name} is not an all-rounder.")

# Print the player's personal info
print(player.player_info)


