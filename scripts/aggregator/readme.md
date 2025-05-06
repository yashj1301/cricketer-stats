
# 📦 Module: Aggregator

The `aggregator.py` module handles the aggregation of multiple players' transformed statistics into **master datasets** for each stat type. This allows easy historical analysis and simplifies downstream dashboarding.

---

## 🧠 What This Module Does

When we scrape and transform player data, we get individual-level stats. But to generate comprehensive insights and enable cross-player comparisons, we need **master datasets**.

This module:

* Appends new player stats to master stats (batting, bowling, fielding, allround, personal info).
* Ensures no duplicates (by checking composite keys like `Inns ID`).
* Sorts and structures the data in an analysis-friendly format.
* Is designed to be reusable across stat types.

---

## 📂 Class: `Aggregator`

```python
agg = Aggregator(bucket_name, player_name, player_id)
```

### 🔧 Parameters:

| Parameter     | Type | Description                                           |
| ------------- | ---- | ----------------------------------------------------- |
| `bucket_name` | str  | Name of the AWS S3 bucket                             |
| `player_name` | str  | Name of the player (for logging/tracking)             |
| `player_id`   | str  | Unique ID of the player, used for identifying entries |

---

## 🔁 Attributes:

Each stat type has **two sets of attributes**:

* `*_concat` — New transformed data (to be added to the master sheet).
* `*_master` — Existing master data downloaded from S3.

| Attribute Name    | Description                           |
| ----------------- | ------------------------------------- |
| `batting_concat`  | New batting records to add            |
| `bowling_concat`  | New bowling records to add            |
| `fielding_concat` | New fielding records to add           |
| `allround_concat` | New allround records to add           |
| `info_concat`     | New personal info to add              |
| `batting_master`  | Full existing master batting dataset  |
| `bowling_master`  | Full existing master bowling dataset  |
| `fielding_master` | Full existing master fielding dataset |
| `allround_master` | Full existing master allround dataset |
| `info_master`     | Full existing player info dataset     |

---

## ⚙️ Methods

### 1. `prepare_concat_df(tf_df, stat_type)`

Prepares the transformed DataFrame for appending by:

* Making a copy
* Adding `Player ID` and a composite `Inns ID` for uniqueness (except for personal\_info)

```python
agg.prepare_concat_df(tf_loader.battingstats, "batting")
```

---

### 2. `merge_df(master_df, concat_df, dedup_keys, sort_keys)`

Safely merges new rows into the master sheet. It:

* Concatenates both DataFrames
* Drops duplicates using `dedup_keys`
* Sorts using `sort_keys`
* Resets index

```python
agg.merge_df(existing_master, new_df, dedup_keys=["Inns ID"], sort_keys=["Player ID", "Start Date"])
```

---

### 3. `run_agg(stat_type)`

Runs the aggregation logic end-to-end for a specified stat type.

* Supports `'batting'`, `'bowling'`, `'fielding'`, `'allround'`, `'personal_info'`, or `'all'`.
* Internally calls both `prepare_concat_df()` and `merge_df()`.

```python
agg.run_agg("batting")
agg.run_agg("all")  # for all stats
```

---

## 🧪 Sample Usage

```python
from loader import LoadData
from aggregator import Aggregator
from scraper import ScrapeData

player_name = "Jacques Kallis"
bucket_name = "cricketer-stats"
stat_type = "all"

# Step 1: Download data
tf_loader = LoadData(player_name, data_type="tf")
tf_loader.load_data(bucket_name, load_type="download", stat_type=stat_type)
if tf_loader.player_info is None:
    tf_loader.load_data(bucket_name, load_type="download", stat_type="personal_info")
player_id = tf_loader.player_info['Player ID'][0]

# Step 2: Download master sheet
master_loader = LoadData(player_name, data_type="tf", master=True)
master_loader.load_data(bucket_name, load_type="download", stat_type=stat_type)

# Step 3: Aggregator initialization
agg = Aggregator(bucket_name, player_name, player_id)

# Step 4: Assign dataframes
agg.batting_concat = tf_loader.battingstats
agg.batting_master = master_loader.battingstats
# (do the same for other stats...)

# Step 5: Run aggregation
agg.run_agg(stat_type="all")

# Step 6: Upload back to S3
master_loader.battingstats = agg.batting_master
master_loader.load_data(bucket_name, load_type="upload", stat_type=stat_type)
```

---

## ✅ Best Practices

* Always check if `player_info` is available before accessing `player_id`.
* Call `agg.run_agg('personal_info')` explicitly when stat\_type is not `"all"`.
* Use `Inns ID` as a composite key: `"Player ID + Format + Match ID + Innings Number"`

---