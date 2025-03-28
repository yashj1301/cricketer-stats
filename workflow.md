## Cricketer Stats Pipeline – Deployment Workflow


### 1. Objective
---
To build and deploy a modular data pipeline that scrapes, transforms, and loads cricketer statistics to Google Cloud Storage (GCS), using Docker for isolation, GitHub Actions for CI/CD, and Google Cloud Composer (Airflow) for orchestration.

---
### 2. Key Components
---

- **Driver Scripts:**
  - `scraper_test.py`: Scrapes player data and loads raw data to GCS.
  - `transformer_test.py`: Downloads raw data from GCS, transforms it, and uploads cleaned data.

- **Docker Architecture:**
  - **Base Image**:
    - Uses `python:3.x-slim` as the base.
    - Installs all required Python libraries via `requirements.txt`.
    - Sets up environment variables.
    - Configures service account key for Google Cloud authentication.
  - **Service-Specific Images**:
    - `scraper_test` image runs `scraper_test.py`.
    - `transformer_test` image runs `transformer_test.py`.

- **Google Artifact Registry**: Stores and version-controls the Docker images.

- **Google Cloud Composer**: Executes and manages the task flow using Airflow DAGs.

- **GitHub Actions**: Detects changes, builds Docker images, pushes them to Artifact Registry, and triggers Composer.

---
### 3. Workflow Steps
---

#### Step 1: Code Push
- Developer pushes code changes to the GitHub repository (`dev` or `main` branch).

#### Step 2: GitHub Actions
- Automatically triggered by a Git push.
- Authenticates to Google Cloud using a service account key from GitHub Secrets.
- Builds two Docker images:
  - One for `scraper_test.py`
  - One for `transformer_test.py`
- Pushes both images to Google Artifact Registry.
- Triggers the Cloud Composer DAG manually using `gcloud composer environments run`.

#### Step 3: Cloud Composer DAG Execution
- DAG has two sequential tasks:
  - **Task 1:** Executes the scraper Docker image from Artifact Registry.
  - **Task 2:** Executes the transformer Docker image (after Task 1 completes).
- Each task runs inside a container that reads/writes to Google Cloud Storage.

#### Step 4: Power BI Connectivity
- Final transformed datasets are available in GCS.
- Power BI connects to the bucket (directly or via local sync) to display updated dashboards.


---
### 4. Authentication Setup
---
#### GitHub Actions
- Create a Google Cloud service account with the following roles:
  - `Artifact Registry Writer`
  - `Composer User`
  - `Storage Admin` (if data access is needed)
- Download the service account key (JSON).
- Add the following GitHub Secrets:
  - `GCP_SA_KEY` – full contents of the JSON key
  - `GCP_PROJECT_ID`
  - `GCP_REGION`

#### Local Docker Testing
- Mount or copy the service account key file into the container.
- Set the environment variable inside the Dockerfile or script:
  ```
  ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"
  ```

#### Cloud Composer
- No special configuration needed.
- It uses its environment's default service account with permissions.


