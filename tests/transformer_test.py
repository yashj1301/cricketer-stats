from loader import LoadData
from transformer import TransformData

def main():
    # ─────────── CONFIG ───────────
    player_name = "Virat Kohli"
    bucket_name = "cricketer-stats"   
    # ───────────────────────────────

    print(f"[TRANSFORMER] Downloading raw data for {player_name!r} from bucket {bucket_name!r}...")
    raw_loader = LoadData(player_name, data_type="raw")
    transformer = TransformData(player_name)

    raw_loader.load_data(bucket_name, load_type="download")

    transformer.battingstats  = raw_loader.battingstats
    transformer.bowlingstats  = raw_loader.bowlingstats
    transformer.fieldingstats = raw_loader.fieldingstats
    transformer.allroundstats = raw_loader.allroundstats
    transformer.player_info   = raw_loader.player_info

    print(f"[TRANSFORMER] Transforming data for {player_name!r}...")
    transformer.process_data()

    print(f"[TRANSFORMER] Uploading transformed data for {player_name!r} to bucket {bucket_name!r}...")
    tf_loader = LoadData(player_name, data_type="tf")

    tf_loader.battingstats   = transformer.battingstats
    tf_loader.bowlingstats   = transformer.bowlingstats
    tf_loader.fieldingstats  = transformer.fieldingstats
    tf_loader.allroundstats  = transformer.allroundstats
    tf_loader.player_info    = transformer.player_info

    tf_loader.load_data(bucket_name, load_type="upload")

    print(f"[TRANSFORMER] Done for {player_name!r}.")

if __name__ == "__main__":
    main()
