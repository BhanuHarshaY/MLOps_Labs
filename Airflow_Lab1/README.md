# Airflow Lab 1 - Mall Customer Segmentation
Author: Bhanu Harsha Y
---
An Apache Airflow pipeline that automates K-Means clustering on the Mall Customers dataset to determine the optimal number of customer segments using the **Elbow Method**. The pipeline runs entirely inside Docker — no local Python installation required.

---

## Project Structure

```
airflow_lab1/
├── config/
├── dags/
│   ├── data/
│   │   ├── file.csv        # Full Mall Customers dataset (200 records)
│   │   └── test.csv        # Subset for quick testing (20 records)
│   ├── model/
│   │   └── model.sav       # Saved K-Means model (generated at runtime)
│   ├── src/
│   │   ├── __init__.py
│   │   └── lab.py          # Core ML functions
│   └── airflow.py          # DAG definition
├── logs/
├── plugins/
├── .env
├── docker-compose.yaml
└── README.md
```

---

## DAG Overview: `MallCustomer_Clustering`

The DAG consists of 4 sequential tasks:

```
load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task
```

| Task | Function | Description |
|------|----------|-------------|
| `load_data_task` | `load_data()` | Reads `file.csv`, selects Age, Annual Income & Spending Score features |
| `data_preprocessing_task` | `data_preprocessing()` | Drops nulls, applies StandardScaler normalization |
| `build_save_model_task` | `build_save_model()` | Fits K-Means for k=1–10, computes SSE, saves model to `model/model.sav` |
| `load_model_task` | `load_model_elbow()` | Loads saved model, applies KneeLocator to find optimal clusters |

---

## Prerequisites

- **Docker Desktop** installed and running (allocate at least 4GB RAM)
- **Git** (if pushing to GitHub)

---

## Setup & Running the Lab

### Step 1: Navigate to the lab directory

```bash
cd airflow_lab1
```

### Step 2: Fetch the official Airflow Docker Compose file

```bash
# macOS / Linux
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml'

# Windows (cmd)
curl -o docker-compose.yaml https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml
```

### Step 3: Create required directories

```bash
# macOS / Linux
mkdir -p ./logs ./plugins ./config

# Windows (cmd)
mkdir logs plugins config
```

### Step 4: Set Airflow UID (macOS/Linux only)

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

> On Windows, the `.env` file is already provided with `AIRFLOW_UID=50000`.

### Step 5: Update `docker-compose.yaml`

Find and update the following fields in `docker-compose.yaml`:

```yaml
# Disable example DAGs
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

# Install required Python packages
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- pandas scikit-learn kneed}

# Mount working data directory
- ${AIRFLOW_PROJ_DIR:-.}/working_data:/opt/airflow/working_data

# Set admin credentials
_AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow2}
_AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow2}
```

### Step 6: Initialize the Airflow database

```bash
docker compose up airflow-init
```

> This will take a few minutes on first run.

### Step 7: Start Airflow

```bash
docker compose up
```

Wait until you see:
```
airflow-webserver-1  | 127.0.0.1 - - [date] "GET /health HTTP/1.1" 200 ...
```

### Step 8: Access the Airflow UI

- Open your browser and go to: [http://localhost:8080](http://localhost:8080)
- Login with:
  - **Username:** `airflow2`
  - **Password:** `airflow2`

### Step 9: Trigger the DAG

1. Find `MallCustomer_Clustering` in the DAGs list
2. Click the **Trigger DAG** button (▶) or toggle the switch to **On**
3. Monitor task progress in the **Graph** view

### Step 10: View Results

1. Click on `MallCustomer_Clustering` → **Graph** tab
2. Click `load_model_task` → **Logs** tab
3. Look for the output line:
   ```
   Optimal number of clusters (Elbow Method): X
   ```

### Step 11: Stop Airflow

```bash
docker compose down
```

---

## Dataset

**Mall Customers Dataset** — 200 records with features:
- `Age` — Customer age
- `Annual_Income` — Annual income in $k
- `Spending_Score` — Store-assigned spending behavior score (1–100)

The pipeline uses all three numeric features for clustering after standardization.

---

## GitHub Setup

If pushing to your `MLOps_Labs` repo, add the following to `.gitignore`:

```
__pycache__/
*.pyc
logs/
plugins/
config/
dags/model/model.sav
.env
docker-compose.yaml
```

---

## Dependencies

All packages are installed automatically inside the Docker container via `_PIP_ADDITIONAL_REQUIREMENTS`:

| Package | Purpose |
|---------|---------|
| `pandas` | Data loading and manipulation |
| `scikit-learn` | StandardScaler and KMeans |
| `kneed` | KneeLocator for elbow method detection |
