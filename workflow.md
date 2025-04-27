## Cricketer Stats Pipeline – Deployment Workflow


### 1. Objective
---
To build and deploy a modular data pipeline that scrapes, transforms, and loads cricketer statistics to AWS S3 Bucket, using Docker for isolation, GitHub Actions for CI/CD, and MWAA for orchestration.

---
### 2. Key Components
---

- **Driver Scripts:**
  - `scraper_test.py`: Scrapes player data and loads raw data to AWS S3.
  - `transformer_test.py`: Downloads raw data from AWS S3, transforms it, and uploads cleaned data.

- **Docker Architecture:**
  - **Base Image**:
    - Uses `python:3.x-slim` as the base.
    - Installs all required Python libraries via `requirements.txt`.
    - Sets up environment variables.
    - Configures environment variables for AWS variables. 
  - **Service-Specific Images**:
    - `cricketer-stats-scraper` image runs `scraper_test.py`.
    - `cricketer-stats-transformer` image runs `transformer_test.py`.

- **Elastic Container Registry**: Stores and version-controls the Docker images.

- **MWAA (Managed Workloads for Apache Airflow)**: Executes and manages the task flow using Airflow DAGs.

- **GitHub Actions**: Detects changes, builds Docker images, pushes them to ECR, and triggers MWAA.

---
### 3. Workflow Steps
---

#### Step 1: Code Push
- Developer pushes code changes to the GitHub repository (`dev` or `main` branch).

#### Step 2: GitHub Actions
- Automatically triggered by a Git push.
- Authenticates AWS using the access key in the .env file. 
- Builds two Docker images:
  - One for `scraper_test.py`
  - One for `transformer_test.py`
- Pushes both images to ECR.
- Triggers the Airflow DAG through MWAA.

#### Step 3: Airflow DAG Execution
- DAG has two sequential tasks:
  - **Task 1:** Executes the scraper Docker image from ECR.
  - **Task 2:** Executes the transformer Docker image (after Task 1 completes).
- Each task runs inside a container that reads/writes to AWS S3.

#### Step 4: Power BI Connectivity
- Final transformed datasets are available in S3.
- Power BI connects to the bucket (either through Athena or local Python script) to display updated dashboards.

---
### 4. Authentication Setup (AWS)
---

#### GitHub Actions  
1. **Create an IAM user** in your AWS account with only the permissions your pipeline needs, for example:  
   - `AmazonS3FullAccess` (for reading/writing your buckets)  
   - `AmazonECRFullAccess` (if you push/pull Docker images)  
   - `AmazonMWAAFullAccess` (if you deploy or update MWAA DAGs)  
2. **Generate an access key** (Access Key ID & Secret Access Key) for that user.  
3. In your GitHub repository, go to **Settings → Secrets and variables → Actions → New repository secret**, and add:  
   - `AWS_ACCESS_KEY_ID`  
   - `AWS_SECRET_ACCESS_KEY`  
   - `AWS_REGION`

#### Local Docker Testing  
_(to be determined)_
#### MWAA (Managed Workflows for Apache Airflow)  
_(to be determined)_
