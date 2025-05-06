import pandas as pd
import boto3
from botocore.exceptions import ClientError
from io import StringIO
from dotenv import load_dotenv
import os

load_dotenv()  # Load AWS credentials from .env

s3 = boto3.client("s3")

class LoadData:

    def __init__(self, player_name=None, data_type=None, master=False):
        
        """
        Initializes the CricketerStatsLoader with player name and data type.
        Args:
            player_name (str): Name of the player.
            data_type (str): Type of data ('raw' or 'tf').
            master (bool): Flag to indicate if the data is for the master sheet.
        """

        self.player_name = player_name.lower().replace(" ", "_") if player_name else None
        self.data_type = data_type  # 'raw' or 'tf'
        self.battingstats = None
        self.bowlingstats = None
        self.fieldingstats = None
        self.allroundstats = None
        self.player_info = None

        self.master = master      

        # Mapping of stat types to file names
        self.file_name_map = {
            "batting": "batting_stats.csv",
            "bowling": "bowling_stats.csv",
            "fielding": "fielding_stats.csv",
            "allround": "allround_stats.csv",
            "personal_info": "personal_info.csv"
        }
  
    def get_object_key(self, stat_type):
        return f"master/{self.file_name_map[stat_type]}" if self.master \
           else f"players_data/{self.player_name}/{self.data_type}/{self.file_name_map[stat_type]}"


    def ensure_bucket_exists(self, bucket_name, flag=0):

        """Checks if the S3 bucket exists, and creates it if not."""
        
        try:
            s3.head_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' already exists.")
        
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            
            if error_code == 404:
                print(f"Bucket '{bucket_name}' does not exist.")

                if flag == 1:
                    
                    print(f"Creating bucket '{bucket_name}'...")
                    s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': os.getenv("AWS_DEFAULT_REGION")
                                                }
                    )
                    print(f"Bucket '{bucket_name}' created successfully.")
            
            else: raise e
    
    def upload_df(self, bucket_name, stat_type, df):

        """Uploads a Pandas DataFrame as a CSV file to S3."""
    
        if stat_type not in self.file_name_map:
            print(f" Invalid stat_type '{stat_type}'.")
            return None

        object_key = self.get_object_key(stat_type)

        if df is None or df.empty:
            print(f"Warning: {stat_type} dataframe is empty, skipping upload.")
            return

        try:
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            s3.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=csv_buffer.getvalue(),
                ContentType="text/csv"
            )
            
            print(f" Uploaded to s3://{bucket_name}/{object_key}")
        
        except Exception as e:
            print(f"Error uploading {stat_type} stats to {bucket_name}/{object_key}: {e}")
            return None

    def download_df(self, bucket_name, stat_type):

        """Downloads a cricket stat CSV from S3 into a DataFrame."""


        if stat_type not in self.file_name_map:
            print(f" Invalid stat_type '{stat_type}'.")
            return None

        object_key = self.get_object_key(stat_type)
        
        try:

            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            content = response["Body"].read().decode("utf-8")
            df = pd.read_csv(StringIO(content))
            print(f" Downloaded from s3://{bucket_name}/{object_key}")
            return df
        
        except Exception as e:
            print(f"Error downloading {stat_type} stats from {bucket_name}/{object_key}: {e}")
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

        # Perform the upload operation
        if load_type == "upload":

            # Ensure the S3 bucket exists
            self.ensure_bucket_exists(bucket_name,flag=1)

            if not self.master: print(f"Uploading {self.player_name}'s {self.data_type} {stat_type} data to S3...")
            else: print(f"Uploading master {stat_type} data to S3...")

            if self.battingstats is not None and stat_type in ["all", "batting"]:
                self.upload_df(bucket_name, "batting", self.battingstats)

            if self.bowlingstats is not None and stat_type in ["all", "bowling"]:
                self.upload_df(bucket_name, "bowling", self.bowlingstats)

            if self.fieldingstats is not None and stat_type in ["all", "fielding"]:
                self.upload_df(bucket_name, "fielding", self.fieldingstats)

            if self.allroundstats is not None and stat_type in ["all", "allround"]:
                self.upload_df(bucket_name, "allround", self.allroundstats)

            if self.player_info is not None and stat_type in ["all", "personal_info"]:
                self.upload_df(bucket_name, "personal_info", self.player_info)

            if not self.master: print(f"{stat_type} {self.data_type} data uploaded to s3://{bucket_name}/{self.player_name}/{self.data_type}/")
            else: print(f"master {stat_type} data uploaded to s3://{bucket_name}/master/")
        
        
        # Perform the download operation
        elif load_type == "download":

            # Ensure the S3 bucket exists
            self.ensure_bucket_exists(bucket_name)

            if not self.master: print(f"Downloading {self.player_name}'s {self.data_type} {stat_type} data from S3...")
            else: print(f"Downloading master {stat_type} data from S3...")

            if stat_type in ["all", "personal_info"]:
                self.player_info = self.download_df(bucket_name, "personal_info")

            if stat_type in ["all", "batting"]:
                self.battingstats = self.download_df(bucket_name, "batting")

            if stat_type in ["all", "bowling"]:
                self.bowlingstats = self.download_df(bucket_name, "bowling")

            if stat_type in ["all", "fielding"]:
                self.fieldingstats = self.download_df(bucket_name, "fielding")

            if stat_type in ["all", "allround"]:
                
                # ─────────── NORMAL (player-wise) ───────────
                if not self.master:
                    if self.player_info is None or self.player_info.empty:
                        print(f"Warning: Player info not found for {self.player_name}. Skipping allround stats download.")
                        self.allroundstats = None

                    elif "Allrounder" in self.player_info["PLAYING ROLE"].values:
                        self.allroundstats = self.download_df(bucket_name, "allround")

                    else:
                        print(f"Player {self.player_name} is not an Allrounder. Skipping allround stats download.")
                        self.allroundstats = None

                # ─────────── MASTER ───────────
                else:
                    # Master case - try download directly
                    self.allroundstats = self.download_df(bucket_name, "allround")
                    
                
            if not self.master: print(f"{stat_type} {self.data_type} data downloaded from s3://{bucket_name}/{self.player_name}/{self.data_type}/")
            else: print(f"master {stat_type} data downloaded from s3://{bucket_name}/master/")