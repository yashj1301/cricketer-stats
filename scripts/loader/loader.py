import pandas as pd
import boto3
import botocore.exceptions
from io import StringIO
from dotenv import load_dotenv
import os

load_dotenv()  # Load AWS credentials from .env

s3 = boto3.client("s3")

class LoadData:

    def __init__(self, player_name, data_type="raw"):
        
        """
        Initializes the CricketerStatsLoader with player name and data type.
        Args:
            player_name (str): Name of the player.
            data_type (str): Type of data ('raw' or 'tf').
        """

        self.player_name = player_name.lower().replace(" ", "_")
        self.data_type = data_type  # 'raw' or 'tf'
        self.battingstats = None
        self.bowlingstats = None
        self.fieldingstats = None
        self.allroundstats = None
        self.player_info = None

    def ensure_bucket_exists(self, bucket_name):

        """Checks if the S3 bucket exists, and creates it if not."""
        
        try:
            s3.head_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' already exists.")
        
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            
            if error_code == 404:
                print(f"⚠️ Bucket '{bucket_name}' does not exist. Creating...")
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': os.getenv("AWS_DEFAULT_REGION")
                                            }
                )
                
                print(f"✅ Bucket '{bucket_name}' created successfully.")
            
            else: raise e
    
    def upload_df(self, bucket_name, object_key, df):

        """Uploads a Pandas DataFrame as a CSV file to S3."""

        if df is None or df.empty:
            print(f"Warning: {object_key} is empty, skipping upload.")
            return

        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )

        print(f" Uploaded to s3://{bucket_name}/{object_key}")

    def download_df(self, bucket_name, stat_type):

        """Downloads a cricket stat CSV from S3 into a DataFrame."""

        file_name_map = {
            "batting": "batting_stats.csv",
            "bowling": "bowling_stats.csv",
            "fielding": "fielding_stats.csv",
            "allround": "allround_stats.csv",
            "personal_info": "personal_info.csv"
        }

        '''If 'all' is passed, download all stat types
        if stat_type == "all":
            data = {}
            for stat in file_name_map:
                data[stat] = self.download_df(bucket_name, stat)  # Recursively call download_df for each type
            return data
        '''

        if stat_type not in file_name_map:
            print(f" Invalid stat_type '{stat_type}'.")
            return None

        object_key = f"{self.player_name}/{self.data_type}/{file_name_map[stat_type]}"

        try:

            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            content = response["Body"].read().decode("utf-8")
            df = pd.read_csv(StringIO(content))
            print(f" Downloaded from s3://{bucket_name}/{object_key}")
            return df
        
        except Exception as e:
            print(f"Error downloading {stat_type} stats: {e}")
            return None

    def load_data(self, bucket_name, load_type, stat_type="all"):
    
        """
        Loads cricket stats data to/from S3.

        Args:
            bucket_name (str): Name of the S3 bucket.
            load_type (str): Type of load operation ('upload' or 'download').
            stat_type (str): Type of stats to load ('all', 'batting', 'bowling', 'fielding', 'allround', 'personal_info').
        """            
        
        if load_type not in ["upload", "download"]:
            print(f"Invalid load type '{load_type}'. Must be 'upload' or 'download'.")
            return

        if stat_type not in ["all", "batting", "bowling", "fielding", "allround", "personal_info"]:
            print(f"Invalid stat type '{stat_type}'. Must be 'all', 'batting', 'bowling', 'fielding', 'allround', or 'personal_info'.")
            return

        # Ensure the S3 bucket exists
        self.ensure_bucket_exists(bucket_name)

        # Perform the upload operation
        if load_type == "upload":

            print(f"Uploading {self.player_name}'s {self.data_type} {stat_type} data to S3...")
            
            base_folder = f"{self.player_name}/{self.data_type}/"

            if self.battingstats is not None and stat_type in ["all", "batting"]:
                self.upload_df(bucket_name, base_folder + "batting_stats.csv", self.battingstats)

            if self.bowlingstats is not None and stat_type in ["all", "bowling"]:
                self.upload_df(bucket_name, base_folder + "bowling_stats.csv", self.bowlingstats)

            if self.fieldingstats is not None and stat_type in ["all", "fielding"]:
                self.upload_df(bucket_name, base_folder + "fielding_stats.csv", self.fieldingstats)

            if self.allroundstats is not None and stat_type in ["all", "allround"]:
                self.upload_df(bucket_name, base_folder + "allround_stats.csv", self.allroundstats)

            if self.player_info is not None and stat_type in ["all", "personal_info"]:
                self.upload_df(bucket_name, base_folder + "personal_info.csv", self.player_info)

            print(f"All {self.data_type} data uploaded to s3://{bucket_name}/{base_folder}")

        # Perform the download operation
        elif load_type == "download":

            print(f"Downloading {self.player_name}'s {self.data_type} data from S3...")

            if stat_type in ["all", "personal_info"]:
                self.player_info = self.download_df(bucket_name, "personal_info")

            if stat_type in ["all", "batting"]:
                self.battingstats = self.download_df(bucket_name, "batting")

            if stat_type in ["all", "bowling"]:
                self.bowlingstats = self.download_df(bucket_name, "bowling")

            if stat_type in ["all", "fielding"]:
                self.fieldingstats = self.download_df(bucket_name, "fielding")

            if stat_type in ["all", "allround"]:

                # Download allround stats if PLAYING ROLE is "Allrounder"
                if self.player_info is not None and "Allrounder" in self.player_info["PLAYING ROLE"].values:
                    self.allroundstats = self.download_df(bucket_name, "allround")
                
                else:
                    print(f"Warning: Player {self.player_name} is not an Allrounder. Skipping allround stats download.")
                    self.allroundstats = None
                
            print(f"All {self.data_type} data downloaded from s3://{bucket_name}/{self.player_name}/{self.data_type}/")
