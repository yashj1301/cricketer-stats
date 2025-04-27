## Documentation for `loader.py`

### Overview

The `loader.py` script defines the **`LoadData`** class, which manages uploading and downloading of cricketer statistics to and from an AWS S3 bucket. It supports both raw and transformed data, and will create the target bucket on upload if it does not already exist.

---

### Requirements

- **pandas**  
- **boto3**  
- **python-dotenv**  
- **io** (standard library)  
- **os** (standard library)

Make sure to have a `.env` file (git-ignored) in the project root with:
```bash
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=...
```
and call `load_dotenv()` before using boto3.

### Class Definition
```python
class LoadData:
    def __init__(self, player_name: str, data_type: str = "raw"):
        ...
    def ensure_bucket_exists(self, bucket_name: str, flag: int):
        ...
    def upload_df(self, bucket_name: str, object_key: str, df: pd.DataFrame):
        ...
    def download_df(self, bucket_name: str, stat_type: str) -> Optional[pd.DataFrame]:
        ...
    def load_data(self, bucket_name: str, load_type: str, stat_type: str = "all"):
        ...
```
#### 1. Constructor

```python
def __init__(self, player_name: str, data_type: str = "raw"):
    """
    Args:
      player_name: e.g. "Virat Kohli" (will be normalized to lowercase/underscores)
      data_type:   "raw" or "tf" (transformed)
    """
```

It stores the player name and data type ("raw" or transformed, i.e. "tf"), initialize placeholders for each stats DataFrame.

#### 2. `ensure_bucket_exists()`

```python
def ensure_bucket_exists(self, bucket_name: str, flag: int):
    """
    - Checks if `bucket_name` exists in S3.
    - On upload (checked through flag = 1), if missing, creates it in AWS_DEFAULT_REGION.
    """
```

It calls `s3.head_bucket()` to check bucket existence. If a __404/NoSuchBucket__ error is returned, it calls `s3.create_bucket()` with the region from `AWS_DEFAULT_REGION` only on upload (this is checked through flag=1); Otherwise re-raises unexpected errors.

#### 3. `upload_df()`

```python
def upload_df(self, bucket_name: str, object_key: str, df: pd.DataFrame):
    """
    Uploads the given DataFrame as CSV to S3 at `s3://{bucket_name}/{object_key}`.
    - Skips if df is None or empty.
    """
```

It serializes `df.to_csv()` into an in-memory buffer and put the object, i.e. uploads to S3 bucket.  
Prints a warning if the DataFrame is empty; prints the S3 path on success.

#### 4. `download_df()`

```python
def download_df(self, bucket_name: str, stat_type: str) -> Optional[pd.DataFrame]:
    """
    Downloads a single stats CSV from:
      s3://{bucket_name}/{player_name}/{data_type}/{<stat_type>_stats.csv}
    and returns it as a pandas.DataFrame, or None on error.
    """
```

For this function, __`stat_type`__ must be one of: ["batting", "bowling", "fielding", "allround", "personal_info"].

It builds the object key from player name, data type, and a lookup map.
Reads the S3 object body, decodes to UTF-8, and implements `pd.read_csv()` from a StringIO.  
Prints the S3 path on success.

#### 5. `load_data()`

```python
def load_data(self, bucket_name: str, load_type: str, stat_type: str = "all"):
    """
    High-level method for upload/download of one or all stat types.
    
    Args:
      bucket_name: the S3 bucket name
      load_type:   "upload" or "download"
      stat_type:   "all" or any single stat_type (batting, bowling, etc.)
    """
```
__Flow:__

1. It Validates load_type [upload, download] and stat_type [all, batting, bowling, fielding, allround, personal_info]. 
2. It then calls `ensure_bucket_exists(bucket_name)`.
3. On upload only, if the bucket is missing, it will be created. Else, nothing. 
4. For upload: iterate through each non-None DataFrame attribute (battingstats, bowlingstats, etc.) and call `upload_df()`.
5. For download: call `download_df()` for each requested stat type and assign back to the corresponding class attribute.

### Usage Example 

```python
from loader import LoadData

# 1. Scrape or generate your DataFrames
player = "Virat Kohli"
raw_loader = LoadData(player, data_type="raw")
raw_loader.battingstats = scraped_batting_df
raw_loader.bowlingstats = scraped_bowling_df
# … assign other stats …

# 2. Upload raw data to S3
raw_loader.load_data(bucket_name="cricketer-stats", load_type="upload", stat_type="all")

# 3. Later, download raw data back into memory
raw_loader = LoadData(player, data_type="raw")
raw_loader.load_data(bucket_name="cricketer-stats", load_type="download", stat_type="all")
print(raw_loader.battingstats.head())
```












