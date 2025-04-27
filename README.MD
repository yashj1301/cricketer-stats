## Project - Cricketer Stats Analysis

### Overview
This project contains a cricket statistics scraper built with Python to extract detailed player data from ESPN CricInfo. The scraper collects various stats, including batting, bowling, all-rounder performance, fielding stats, and personal information about cricketers.

The scraper uses __Selenium__ for web scraping and __pandas__ for data management. It further uses __boto3__ for connection with AWS S3 buckets. 

The data collected is stored in AWS S3 Buckets and displayed through Power BI dashboards.

### Features

1. Scrapes player statistics: Batting, Bowling, All-Rounder, and Fielding.
2. Extracts personal information: Name, Age, Country, Playing Role.
3. Uses Selenium for scraping and pandas for data manipulation.
4. Designed to be modular, allowing for easy integration with databases or visual tools.

### Project Files

- **`setup.py`**  
  Defines this project as a Python package.  
  - Specifies metadata (name, version, author, etc.)  
  - Reads dependencies from `requirements.txt`  
  - Allows us to install your scraper/transformer/loader modules with:
    ```bash
    pip install -e . # from project root directory
    ```
  so we can import them as `from scraper import ScrapeData`, etc., anywhere on our local development environment. 

- **`workflow.md`**  
  Describes the end-to-end pipeline steps at a glance:  
  1. Code pushed to GitHub → GitHub Actions builds and pushes Docker images.   
  2. Images are deployed and DAGs updated in MWAA (Airflow).   
  3. MWAA pulls the images and runs the scraper/transformer/loader containers.  
  4. Final data lands in S3 and is consumed by Power BI  
  
  It’s your “single source of truth” for how all the pieces fit together.

- **`extras.txt`**  
  A rolling backlog of future enhancements and feature ideas, for example:  
  - dynamic fetching of ground names and their images
  - incremental loading of data
  - custom exceptions
  - inheritance between the 3 classes
  - using secret managers for confidential data. 
  
  This keeps our “nice-to-haves” captured without cluttering the core code.
