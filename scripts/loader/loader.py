import pandas as pd
from google.cloud import storage
from io import BytesIO

class CricketerStatsLoader:
    def __init__(self, player_name, data_type="raw"):
        self.player_name = player_name.lower().replace(" ", "_")
        self.data_type = data_type  # 'raw' or 'tf'
        self.battingstats = None
        self.bowlingstats = None
        self.fieldingstats = None
        self.allroundstats = None
        self.player_info = None

    def ensure_bucket_exists(self, bucket_name):
        """Checks if the bucket exists; if not, creates it."""
        client = storage.Client()
        bucket = client.lookup_bucket(bucket_name)

        if not bucket:
            print(f"Bucket '{bucket_name}' does not exist. Creating it...")
            bucket = client.create_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

    def upload_df_to_gcs(self, bucket_name, destination_blob_name, df):
        """Uploads a Pandas DataFrame as a CSV file to Google Cloud Storage."""
        if df is None or df.empty:
            print(f"Warning: {destination_blob_name} is empty, skipping upload.")
            return

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Convert DataFrame to CSV in memory (Binary Buffer)
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)  # Reset buffer position

        # Upload directly from memory
        blob.upload_from_file(buffer, content_type="text/csv")
        print(f"File uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")

    def download_df_from_gcs(self, bucket_name, stat_type):
        """Downloads a specific type of cricket stats from GCS into a Pandas DataFrame.
    
        Args:
            bucket_name (str): Google Cloud Storage bucket name.
            stat_type (str): Type of data to fetch (e.g., "batting", "bowling", "fielding", "allround", "personal_info").
    
        Returns:
            pd.DataFrame: The downloaded DataFrame, or None if the file is missing.
        """
        # Construct the full GCS path based on the player name, data type, and stat type
        file_name_map = {
            "batting": "batting_stats.csv",
            "bowling": "bowling_stats.csv",
            "fielding": "fielding_stats.csv",
            "allround": "allround_stats.csv",
            "personal_info": "personal_info.csv"
                        }

        if stat_type not in file_name_map:
            print(f"Error: Invalid stat_type '{stat_type}'. Choose from {list(file_name_map.keys())}.")
            return None

        # Define the GCS blob name based on the structure
        source_blob_name = f"{self.player_name}/{self.data_type}/{file_name_map[stat_type]}"

        # Initialize GCS client and fetch the file
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        try:
            csv_data = blob.download_as_text()
            df = pd.read_csv(BytesIO(csv_data.encode()))
            print(f"Successfully downloaded {stat_type} data from gs://{bucket_name}/{source_blob_name}")
            return df
        except Exception as e:
            print(f"Error downloading {stat_type} stats: {e}")
            return None


    def load_data(self, bucket_name):
        """
        Uploads data to GCS in a structured format.
        - bucket_name: Name of the GCS bucket.
        """
        print(f"Uploading {self.player_name}'s {self.data_type} data to GCS...")

        # Ensure bucket exists before uploading
        self.ensure_bucket_exists(bucket_name)

        # Define the base folder (`player_name/raw/` or `player_name/tf/`)
        base_folder = f"{self.player_name}/{self.data_type}/"

        if self.battingstats is not None:
            self.upload_df_to_gcs(bucket_name, base_folder + "batting_stats.csv", self.battingstats)

        if self.bowlingstats is not None:
            self.upload_df_to_gcs(bucket_name, base_folder + "bowling_stats.csv", self.bowlingstats)

        if self.fieldingstats is not None:
            self.upload_df_to_gcs(bucket_name, base_folder + "fielding_stats.csv", self.fieldingstats)

        if self.allroundstats is not None:
            self.upload_df_to_gcs(bucket_name, base_folder + "allround_stats.csv", self.allroundstats)

        if self.player_info is not None:
            self.upload_df_to_gcs(bucket_name, base_folder + "personal_info.csv", self.player_info)

        print(f"All {self.data_type} data successfully uploaded to GCS in gs://{bucket_name}/{base_folder}")