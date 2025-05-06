# 🏏 Cricketer Stats Analytics Pipeline

A modular Python project to scrape, process, and analyze detailed cricket player statistics from ESPN CricInfo. The data is stored in AWS S3 and visualized using Power BI dashboards.

---

## 🔍 Overview

This project builds an end-to-end data pipeline that:

* Scrapes player-level data (batting, bowling, fielding, all-rounder stats, and personal info)
* Transforms and standardizes the data
* Aggregates it into master datasets
* Uploads it to AWS S3 for dashboarding in Power BI or Tableau

The pipeline is structured using modular Python scripts and classes, with extensibility for containerization and orchestration.

---

## 🔀 Tech Stack

| Tool         | Purpose                    |
| ------------ | -------------------------- |
| **Python**   | Core programming language  |
| **Selenium** | Web scraping from CricInfo |
| **pandas**   | Data transformation        |
| **boto3**    | Interacting with AWS S3    |
| **Power BI** | Dashboard visualization    |

---

## 🔁 Workflow

1. **Scrape data** using Selenium for a specific player.
2. **Transform data** into clean, analysis-ready format.
3. **Aggregate** data across multiple players into master datasets.
4. **Upload to AWS S3** in both raw and transformed forms.
5. **Visualize** insights using Power BI.

---

## 📂 Project Structure

```
cricketer-stats/
├── research lab/                 # Exploratory notebooks or R&D scripts
│   ├── EDA.ipynb                 # EDA Notebook
│   ├── check.ipynv               # notebook for experimentation
├── scripts/                      # Python module folder with core logic
│   ├── scraper/                  # Web scraping module
│   ├── transformer/              # Data cleaning and formatting module
│   |── loader/                   # S3 upload/download logic
│   |── aggregator/               # aggregation logic to generate master dataframes
├── scripts.egg-info/             # Auto-generated metadata for Python packaging
├── tests/                        # Test scripts for modules
│   ├── aggregator_test.py
│   ├── scraper_test.py
│   └── transformer_test.py
├── visuals/                      # Power BI (.pbix) and design elements
├── .env                          # AWS credentials and other environment setup
├── .gitignore
├── extras.md                     # Feature backlog and future plans
├── README.md                     # Project documentation
├── requirements.txt              # List of Python dependencies
├── setup.py                      # Package setup file for pip installation
├── test.py                       # Optional test runner script
├── workflow.md                   # Workflow explanation
```

---

## 📌 Key Features

* 🔍 Scrapes detailed stats: **batting, bowling, fielding, allround**, and **player profile**
* ♻️ Clean modular classes: **ScrapeData, TransformData, LoadData, Aggregator**
* ☁️ Uses AWS S3 as the cloud data store
* 📊 Output ready for Power BI or Tableau
* 🧱 Code structured for easy scaling and future automation

---

## 🚀 Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/cricketer-stats.git
   cd cricketer-stats
   ```
2. Create and configure a `.env` file with your AWS credentials:

   ```env
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_DEFAULT_REGION=ap-south-1
   ```
3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Install the project locally as a package:

   ```bash
   pip install -e .
   ```
5. Run any of the test scripts:

   ```bash
   python tests/aggregator_test.py
   ```

   > ⚠️ Make sure to set `player_name` and `bucket_name` before running the tests.

---

## 🛣 Roadmap & Extras

See `extras.txt` for upcoming enhancements, including:

* Dynamic ground info scraping
* Incremental loading logic
* Secret manager integration
* Docker + Airflow orchestration
* Custom exception handling

---

## 📖 Using as a Local Python Package

This project is structured as an installable package using `setup.py`. This allows you to import the core modules (scraper, loader, transformer, aggregator) anywhere in your system.

### Installation:

From the project root, run:

```bash
pip install -e .
```

### Example Usage:

```python
from scraper import ScrapeData
from transformer import TransformData
```

This makes testing and modular development cleaner, especially across notebooks and scripts.

---

## 📖 For Reference

See `workflow.md` for a high-level overview of the entire ETL-to-dashboard pipeline.

---
