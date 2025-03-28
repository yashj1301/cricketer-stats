from scripts.scraper.scraper import Cricketer_Stats_Scraper as ScrapeData
from scripts.transformer.transformer import Cricketer_Stats_Transformer as TransformData
from scripts.loader.loader import CricketerStatsLoader as LoadData
import pandas as pd

# Example usage:

#scraping data
player_name = "Virat Kohli"
virat_raw = ScrapeData(player_name)
virat_raw.get_player_stats()

#loading raw data to bucket
bucket_name = "cricketer_stats"

virat_raw_loader = LoadData(player_name, data_type="raw")
virat_raw_loader.battingstats = virat_raw.battingstats
virat_raw_loader.bowlingstats = virat_raw.bowlingstats
virat_raw_loader.fieldingstats = virat_raw.fieldingstats
virat_raw_loader.player_info = virat_raw.player_info

virat_raw_loader.load_data(bucket_name)

#downloading raw data from bucket
virat_tf = TransformData(player_name)

virat_tf.battingstats = virat_raw_loader.download_df_from_gcs(bucket_name, "batting")
virat_tf.bowlingstats = virat_raw_loader.download_df_from_gcs(bucket_name, "bowling")
virat_tf.fieldingstats = virat_raw_loader.download_df_from_gcs(bucket_name, "fielding")
virat_tf.allroundstats = virat_raw_loader.download_df_from_gcs(bucket_name, "allround")
virat_tf.player_info = virat_raw_loader.download_df_from_gcs(bucket_name, "personal_info")

#transforming data
virat_tf.process_data()

#loading transformed data to bucket
virat_tf_loader = LoadData(player_name, data_type="tf")

virat_tf_loader.battingstats = virat_tf.battingstats
virat_tf_loader.bowlingstats = virat_tf.bowlingstats
virat_tf_loader.fieldingstats = virat_tf.fieldingstats
virat_tf_loader.allroundstats = virat_tf.allroundstats
virat_tf_loader.player_info = virat_tf.player_info

virat_tf_loader.load_data(bucket_name)
