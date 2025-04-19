from scraper import ScrapeData
from transformer import TransformData
from loader import LoadData
import pandas as pd

# --- 🔹 Step 1: Scrape raw data ---
player_name = "Virat Kohli"
virat_raw = ScrapeData(player_name)
virat_raw.get_player_stats()

# --- 🔹 Step 2: Upload raw data to S3 ---
bucket_name = "cricketer-stats"
virat_raw_loader = LoadData(player_name, data_type="raw")

virat_raw_loader.battingstats = virat_raw.battingstats
virat_raw_loader.bowlingstats = virat_raw.bowlingstats
virat_raw_loader.fieldingstats = virat_raw.fieldingstats
virat_raw_loader.allroundstats = virat_raw.allroundstats
virat_raw_loader.player_info = virat_raw.player_info

virat_raw_loader.load_data(bucket_name, load_type="upload", stat_type="all")

# --- 🔹 Step 3: Download raw data from S3 ---
virat_tf = TransformData(player_name)
virat_tf_loader = LoadData(player_name, data_type="raw")

virat_tf_loader.load_data(bucket_name, load_type="download", stat_type="all")

virat_tf.battingstats = virat_tf_loader.battingstats
virat_tf.bowlingstats = virat_tf_loader.bowlingstats
virat_tf.fieldingstats = virat_tf_loader.fieldingstats
virat_tf.allroundstats = virat_tf_loader.allroundstats
virat_tf.player_info = virat_tf_loader.player_info

# --- 🔹 Step 4: Transform the data ---
virat_tf.process_data()

# --- 🔹 Step 5: Upload transformed data to S3 ---
virat_tf_loader = LoadData(player_name, data_type="tf")

virat_tf_loader.battingstats = virat_tf.battingstats
virat_tf_loader.bowlingstats = virat_tf.bowlingstats
virat_tf_loader.fieldingstats = virat_tf.fieldingstats
virat_tf_loader.allroundstats = virat_tf.allroundstats
virat_tf_loader.player_info = virat_tf.player_info

virat_tf_loader.load_data(bucket_name, load_type="upload", stat_type="all")