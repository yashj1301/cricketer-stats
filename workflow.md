## ⚙️ Cricketer Stats Pipeline – Deployment Workflow

---

### 1. 🎯 Objective

Build and deploy a modular ETL pipeline to scrape, transform, and store cricketer statistics in AWS S3, using:

* **Docker** for environment isolation
* **GitHub Actions** for CI/CD
* **MWAA (Managed Workflows for Apache Airflow)** for orchestration

---

### 2. 🧩 Key Components

#### 🔧 Driver Scripts

* `scraper_test.py`: Scrapes player data and uploads raw stats to AWS S3.
* `transformer_test.py`: Downloads raw stats from S3, transforms them, and uploads clean data.
* `aggregator_test.py`: Aggregates player-wise data into master datasets for dashboarding.

#### 🐳 Docker Architecture

* **Base Image**:

  * Inherits from `python:3.x-slim`
  * Installs dependencies via `requirements.txt`
  * Loads AWS credentials via `.env`

* **Service Containers**:

  * `cricketer-stats-scraper` → runs `scraper_test.py`
  * `cricketer-stats-transformer` → runs `transformer_test.py`
  * `cricketer-stats-aggregator` → runs `aggregator_test.py`

#### 📦 Elastic Container Registry (ECR)

* Stores versioned Docker images.

#### ⛓ MWAA (Airflow DAGs)

* Executes Docker containers via DAG tasks.
* Reads/writes data to/from S3.

#### 🔄 GitHub Actions

* CI/CD pipeline that builds Docker images, pushes them to ECR, and triggers MWAA DAGs.

---

### 3. 🔁 Pipeline Flow

#### 🔹 Step 1: Code Push

* Developer pushes changes to `main` or `dev` branch.

#### 🔹 Step 2: GitHub Actions

* Workflow is triggered on push.
* Loads AWS credentials from GitHub Secrets.
* Builds Docker images for each module.
* Pushes images to ECR.
* Triggers MWAA to run the DAG.

#### 🔹 Step 3: Airflow DAG Execution

* DAG consists of 3 tasks:

  1. `scrape_stats` → pulls `scraper` image from ECR and scrapes data.
  2. `transform_stats` → pulls `transformer` image and processes raw data.
  3. `aggregate_stats` → pulls `aggregator` image and appends to master datasets.

#### 🔹 Step 4: Power BI / Tableau Visualization

* Final transformed data resides in `s3://cricketer-stats/master/`
* Dashboards are refreshed from this bucket (via Athena, APIs, or manual export).

---

### 4. 🔐 AWS Authentication Setup

#### GitHub Actions

1. **Create IAM User** with permissions:

   * `AmazonS3FullAccess`
   * `AmazonECRFullAccess`
   * `AmazonMWAAFullAccess`

2. **Generate Access Keys**

   * Store them as secrets in GitHub:

     * `AWS_ACCESS_KEY_ID`
     * `AWS_SECRET_ACCESS_KEY`
     * `AWS_REGION`

#### Local Docker Testing *(optional)*

* Use `.env` file for AWS credentials.
* Mount `.env` inside container at build/run time.

#### MWAA Integration *(to be finalized)*

* DAG pulls Docker images from ECR.
* Leverages MWAA environment variables for runtime AWS auth.

---

This deployment strategy ensures full automation from data collection to visualization, following best practices in CI/CD and cloud orchestration.
