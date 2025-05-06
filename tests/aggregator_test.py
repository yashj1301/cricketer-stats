from loader import LoadData
from aggregator import Aggregator

def main():
    # ─────────── CONFIG ───────────
    player_name = "Virat Kohli"
    bucket_name = "cricketer-stats"
    stat_type   = "all"  # 'all', 'batting', 'bowling', 'fielding', 'allround', 'personal_info'
    # ───────────────────────────────

    print(f"[AGGREGATOR] Downloading transformed data for {player_name!r}...")
    tf_loader = LoadData(player_name, data_type="tf")
    tf_loader.load_data(bucket_name, load_type="download", stat_type=stat_type)

    # Ensure player_info is available every time
    if stat_type not in ["all","personal_info"]: tf_loader.load_data(bucket_name, load_type="download", stat_type="personal_info")  
    player_id = tf_loader.player_info['Player ID'][0]

    print(f"[AGGREGATOR] Downloading existing master data from bucket {bucket_name!r}...")
    master_loader = LoadData(player_name, data_type="tf", master=True)
    master_loader.load_data(bucket_name, load_type="download", stat_type=stat_type)

    # Initialize Aggregator
    agg = Aggregator(bucket_name, player_name, player_id)

    # ─────────── SET CONCAT DF ───────────
    agg.batting_concat   = tf_loader.battingstats
    agg.bowling_concat   = tf_loader.bowlingstats
    agg.fielding_concat  = tf_loader.fieldingstats
    agg.allround_concat  = tf_loader.allroundstats
    agg.info_concat      = tf_loader.player_info

    # ─────────── SET MASTER DF ───────────
    agg.batting_master   = master_loader.battingstats
    agg.bowling_master   = master_loader.bowlingstats
    agg.fielding_master  = master_loader.fieldingstats
    agg.allround_master  = master_loader.allroundstats
    agg.info_master      = master_loader.player_info

    print(f"[AGGREGATOR] Aggregating data for {player_name!r}...")
    agg.run_agg(stat_type=stat_type)
    if stat_type not in ["all","personal_info"]: agg.run_agg(stat_type="personal_info")

    print(f"[AGGREGATOR] Uploading updated master data to bucket {bucket_name!r}...")
    master_loader.battingstats   = agg.batting_master
    master_loader.bowlingstats   = agg.bowling_master
    master_loader.fieldingstats  = agg.fielding_master
    master_loader.allroundstats  = agg.allround_master
    master_loader.player_info    = agg.info_master

    master_loader.load_data(bucket_name, load_type="upload", stat_type=stat_type)
    if stat_type not in ["all","personal_info"]:
        master_loader.load_data(bucket_name, load_type="upload", stat_type="personal_info")

    print(f"[AGGREGATOR] Done for {player_name!r}.")

if __name__ == "__main__":
    main()
