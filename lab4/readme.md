# MLflow Lab 1 - Experiment Tracking with MLflow

## Overview

This lab demonstrates fundamental MLOps concepts using **MLflow** for experiment tracking, model logging, model serving, and custom artifact creation.

**Dataset:** California Housing (sklearn built-in) — predicting median house values based on demographic and geographic features.

**Models Used:**
- Decision Tree Regressor (starter, serving notebooks)
- Ridge Regression (linear_regression notebook)

> **Note:** The professor's reference implementation uses Iris/Wine datasets. This submission uses the California Housing dataset with different models (Decision Tree, Ridge Regression) to demonstrate independent understanding of MLflow concepts.

## Project Structure

```
lab4/
├── mlflow_lab1/
│   ├── requirements.txt
│   ├── starter.ipynb
│   ├── linear_regression.ipynb
│   ├── serving.ipynb
│   ├── serving.py
│   └── mlruns/              (generated after running notebooks)
└── README.md
```

## Prerequisites

- Python 3.9+
- Jupyter Lab installed
- GitHub Lab-1 completed

## Setup Instructions

### 1. Navigate to the working directory
```bash
cd mlops_labs/lab4/mlflow_lab1
```

### 2. Create and activate a virtual environment
```bash
python -m venv mlflow_lab1_env
source mlflow_lab1_env/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Link virtual environment to Jupyter Lab
```bash
python -m ipykernel install --user --name=mlflow_lab1_env
```

### 5. Launch Jupyter Lab
```bash
jupyter-lab
```

Select **mlflow_lab1_env** as the kernel (Kernel → Change Kernel → mlflow_lab1_env).

## Notebooks & Scripts

### 1. `starter.ipynb` — MLflow Autolog, Model Logging & Loading
- Demonstrates `mlflow.autolog()` for automatic experiment tracking
- Manual model logging with `mlflow.sklearn.log_model()`
- Loading a saved model with `mlflow.sklearn.load_model()`
- Verifying predictions match between original and loaded model

### 2. `linear_regression.ipynb` — Parameter & Metric Logging
- Trains Ridge Regression models with 5 different alpha values (0.01, 0.1, 1.0, 10.0, 100.0)
- Manually logs parameters (`mlflow.log_param()`) and metrics (`mlflow.log_metric()`)
- Compares MSE, RMSE, MAE, and R² across all runs
- Generates comparison visualization saved as `ridge_comparison.png`

### 3. `serving.ipynb` — Model Serving via REST API
- Trains and logs a Decision Tree model
- Serves the model using `mlflow models serve`
- Sends prediction requests via `requests.post()` to the REST endpoint
- Compares served model predictions with local predictions

### 4. `serving.py` — Custom Artifacts
- Creates and logs custom artifacts to MLflow:
  - `extra_pip_requirements.txt` — package dependencies for reproducibility
  - `model_summary.json` — model metadata and evaluation results
  - `feature_importance.csv` — ranked feature importances from the Decision Tree
- Logs the model with `extra_pip_requirements` parameter

## Running the MLflow UI

After running any notebook, view your experiments:

```bash
mlflow ui --port 5001
```

Open http://127.0.0.1:5001 in your browser.

> **macOS Note:** Port 5000 may conflict with AirPlay Receiver. Use port 5001 instead.

## Key MLflow Concepts Demonstrated

| Concept | File | MLflow API |
|---------|------|-----------|
| Autologging | starter.ipynb | `mlflow.autolog()` |
| Manual model logging | starter.ipynb | `mlflow.sklearn.log_model()` |
| Model loading | starter.ipynb | `mlflow.sklearn.load_model()` |
| Parameter logging | linear_regression.ipynb | `mlflow.log_param()` |
| Metric logging | linear_regression.ipynb | `mlflow.log_metric()` |
| Model serving | serving.ipynb | `mlflow models serve` |
| Custom artifacts | serving.py | `mlflow.log_artifact()` |

## Author

Bhanu Harsha Yaddanapudi
