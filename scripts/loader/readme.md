## 📦 `loader.py` Module Documentation

### Overview

The `loader.py` module defines the `LoadData` class, which is responsible for uploading and downloading cricketer statistics to and from AWS S3. This class abstracts the S3 interactions and enables modular loading and storage of player-level and master-level datasets.

It supports the following workflows:

* Uploading raw or transformed player data to S3.
* Downloading existing raw or transformed data from S3.
* Uploading and downloading master datasets.
* Conditional downloading of allrounder stats based on player's role.

It also ensures that the necessary bucket exists before uploading and builds correct object keys based on the player and context.

---

### Requirements

* `pandas`: For DataFrame handling.
* `boto3`: AWS SDK for Python.
* `python-dotenv`: To load AWS credentials from `.env` file.
* `io.StringIO`: To convert DataFrames to in-memory CSV buffers.
* `os`: For accessing environment variables.

### Environment Setup

The AWS credentials must be stored in a `.env` file in the root directory with the following format:

```env
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=ap-south-1
```

---

### Class: `LoadData`

```python
LoadData(player_name: str, data_type: str, master: bool = False)
```

#### Arguments:

* `player_name` (str): Name of the player (e.g., "Virat Kohli"). Converted internally to lowercase and underscores.
* `data_type` (str): Type of data, either `"raw"` or `"tf"`.
* `master` (bool): Flag to handle master-level datasets. If `True`, uses the `master/` directory inside the S3 bucket.

#### Attributes:

The following attributes store the loaded DataFrames:

* `battingstats`, `bowlingstats`, `fieldingstats`, `allroundstats`: Statistic-specific DataFrames.
* `player_info`: DataFrame with personal details.

---

### Methods

#### 1. `get_object_key(stat_type: str) -> str`

Returns the object key (S3 file path) for a given stat type, customized by player and `data_type`, or under `master/` for master datasets.

Examples:

* For player-specific data: `virat_kohli/tf/batting_stats.csv`
* For master datasets: `master/batting_stats.csv`

---

#### 2. `ensure_bucket_exists(bucket_name: str, flag: int = 0)`

Checks if the bucket exists. If not, creates the bucket **only if** `flag = 1`. Used internally in upload operations to avoid redundant creation.

---

#### 3. `upload_df(bucket_name: str, stat_type: str, df: pd.DataFrame)`

Uploads a specific DataFrame as a CSV to S3.

* Automatically builds the correct object key.
* Skips upload if the DataFrame is empty or `None`.
* Logs the upload path for verification.

---

#### 4. `download_df(bucket_name: str, stat_type: str) -> pd.DataFrame | None`

Downloads a CSV file from S3, converts it to a DataFrame.

* If the file exists and is valid, returns the DataFrame.
* If not found or error occurs, prints the error and returns `None`.

---

#### 5. `load_data(bucket_name: str, load_type: str, stat_type: str = "all")`

High-level controller for loading or uploading one or more datasets.

**Arguments:**

* `bucket_name`: S3 bucket name.
* `load_type`: One of `"upload"` or `"download"`.
* `stat_type`: One of `"all"`, `"batting"`, `"bowling"`, `"fielding"`, `"allround"`, or `"personal_info"`.

Performs upload/download on each component based on available data.

---

### 🔁 Special Logic for Allrounders

When downloading `allround_stats.csv`, special handling is done:

* For **player-level** (i.e., `master=False`):

  * If `player_info` is not present, attempts to fetch it.
  * If player's "PLAYING ROLE" is `"Allrounder"`, proceeds with downloading.
  * If not an allrounder, skips with a warning.

* For **master-level** (i.e., `master=True`):

  * Skips allrounder role check and attempts download directly.

---

### ✅ Example Usage

```python
from loader import LoadData

# Download transformed data
loader = LoadData("Virat Kohli", data_type="tf")
loader.load_data("cricketer-stats", load_type="download", stat_type="all")
print(loader.battingstats.head())

# Upload transformed data
loader = LoadData("Virat Kohli", data_type="tf")
loader.battingstats = transformed_batting_df
loader.player_info = player_info_df
loader.load_data("cricketer-stats", load_type="upload", stat_type="all")

# Handle master dataset
master_loader = LoadData(data_type="tf", master=True)
master_loader.battingstats = full_batting_df
master_loader.load_data("cricketer-stats", load_type="upload", stat_type="batting")
```

---

### Notes

* This class is meant to be used inside DAGs or automated jobs.
* Safe guards are in place to skip empty DataFrames.
* Print statements provide traceability for uploads/downloads.

This module provides a clean interface for integrating cloud storage with your local pipeline logic, while ensuring modular expansion and player-wise data control.
