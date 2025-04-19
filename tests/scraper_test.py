from scripts.scraper.scraper import ScrapeData
from scripts.loader.loader import LoadData

def main():
    # ─────────── CONFIG ───────────
    player_name = "Virat Kohli"
    bucket_name = "cricketer-stats"   # ← replace with your actual bucket
    # ───────────────────────────────

    print(f"[SCRAPER] Starting scrape for {player_name!r}...")
    scraper = ScrapeData(player_name)
    scraper.get_player_stats()

    print(f"[SCRAPER] Uploading raw data for {player_name!r} to bucket {bucket_name!r}...")
    loader = LoadData(player_name, data_type="raw")

    loader.battingstats   = scraper.battingstats
    loader.bowlingstats   = scraper.bowlingstats
    loader.fieldingstats  = scraper.fieldingstats
    loader.allroundstats  = scraper.allroundstats
    loader.player_info    = scraper.player_info
    loader.load_data(bucket_name,load_type="upload")

    print(f"[SCRAPER] Done for {player_name!r}.")

if __name__ == "__main__":
    main()
