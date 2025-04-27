## Documentation for `transformer.py`

### Overview

The `transformer.py` module defines the **`TransformData`** class, which cleans and casts raw cricketer innings data into analysis-ready tables. It handles value replacements, column extraction, renaming, date parsing, ID formatting, and explicit dtype casting.

---

### Requirements

- **time** (standard library)  
- **pandas**  
- **numpy**

---

### Class Definition

```python
class TransformData:
    def __init__(self, player_name: str): …
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame: …
    def final_df(self,
                 df: pd.DataFrame,
                 common_cols: list,
                 custom_cols: list) -> pd.DataFrame: …
    def process_data(self, type: str = "all") -> None: …
```

#### 1. Constructor

```python
def __init__(self, player_name: str):
    """
    Args:
      player_name: full name of the cricketer (e.g. "Virat Kohli").
    Side-effects:
      - Sets `self.player_name`.
      - Initializes placeholders: `player_info`, `battingstats`,
        `bowlingstats`, `fieldingstats`, `allroundstats`,
        `player_id`, `player_url` to None.
    """
```

Establishes the object’s state; we must later assign raw DataFrames to the stats attributes before calling `process_data()`.

#### 2. transform_data(self, df)

```python
def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans one raw stats table:
      1. Replaces missing-value tokens (e.g. "*", "DNB", "-", "sub") with NaN.
      2. Splits “Opposition” into `Format` and `Opposition` columns.
      3. Normalizes certain ground names and renames to `Location`.
      4. Casts `Start Date` to datetime64.
      5. Prefixes match numbers with “#” and renames to `Match ID`.
    Returns:
      A cleaned DataFrame.
    """
```

__Parameters:__

`df`: raw innings DataFrame (must contain columns: Opposition, Ground, Start Date, Match id).

__Returns:__ new DataFrame after all five transformation steps.

#### 3. final_df(self, df, common_cols, custom_cols)

```python
def final_df(self,
             df: pd.DataFrame,
             common_cols: list,
             custom_cols: list) -> pd.DataFrame:
    """
    Applies `transform_data()`, selects and reorders columns, and casts dtypes.
    Args:
      common_cols: list of columns present in every stats table
        (e.g. ['Match ID','Start Date','Format','Inns','Opposition','Location'])
      custom_cols: list of stats-specific columns
        (e.g. batting: ['Pos','Runs','BF',…])
    Behavior:
      - Cleans via `transform_data()`.
      - Reorders to: common_cols[:-2] + custom_cols + common_cols[-2:].
      - Casts each column to a pre-defined dtype mapping (Int64, float64, etc.).  
      - Logs any casting failures per column.
    Returns:
      The typed, trimmed DataFrame ready for analysis.
    """
```

__Parameters:__

1. `df`: cleaned DataFrame. ready for data type casting.
2. `common_cols`: always-present fields.
3. `custom_cols`: fields specific to batting, bowling, etc.

__Returns:__ a fully cleaned & typed DataFrame.

#### 4. process_data(self, type="all")

```python
def process_data(self, type: str = "all") -> None:
    """
    Drives end-to-end transformation for one or all stat types.
    Args:
      type: one of "batting","bowling","fielding","allround","all"
    Side-effects:
      - Prints processing status.
      - For each requested type, calls `final_df()` and assigns to
        self.battingstats, self.bowlingstats, self.fieldingstats,
        self.allroundstats.
      - Checks `self.player_info` for “allround” role before processing.
    """
```

__Behavior:__

1. Defines column lists for each stat type.
2. For each selected type or “all”, processes the corresponding DataFrame.
3. Prints success or error messages.

### Usage Example 

```python
from scripts.transformer.transformer import TransformData

# 1. Instantiate
tf = TransformData("Virat Kohli")

# 2. Assign your downloaded raw DataFrames:
tf.player_info    = raw_player_info_df
tf.battingstats   = raw_batting_df
tf.bowlingstats   = raw_bowling_df
tf.fieldingstats  = raw_fielding_df
tf.allroundstats  = raw_allround_df  # optional

# 3. Run full transformation
tf.process_data(type="all")

# 4. Inspect outputs
print(tf.battingstats.dtypes)
print(tf.battingstats.head())
```