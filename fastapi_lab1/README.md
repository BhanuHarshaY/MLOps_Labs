# FastAPI Lab 1 — Breast Cancer Prediction API
Author: Bhanu Harsha Y
---
## Overview
This lab demonstrates how to expose a trained Machine Learning model as a REST API using **FastAPI** and **uvicorn**. A Random Forest Classifier is trained on the Breast Cancer Wisconsin dataset and served as an API that predicts whether a tumor is benign or malignant based on input features.

## Tools & Technologies
- **FastAPI** — modern Python web framework for building APIs
- **uvicorn** — ASGI web server used to serve the FastAPI application
- **scikit-learn** — for training the Random Forest Classifier
- **Pydantic** — for request/response data validation

## Dataset
**Breast Cancer Wisconsin Dataset** (from `sklearn.datasets`)
- 569 samples, 30 features (we use the first 10 mean features)
- Binary classification: Malignant (0) or Benign (1)

## Model
**Random Forest Classifier**
- 100 estimators, random_state=42
- Train/test split: 80/20
- Test Accuracy: ~94.7%

## Project Structure
```
fastapi_lab1/
├── model/
│   └── cancer_model.pkl       # Saved trained model (git-ignored)
├── src/
│   ├── __init__.py
│   ├── data.py                # Pydantic request/response schemas
│   ├── train.py               # Model training script
│   ├── predict.py             # Inference logic
│   └── main.py                # FastAPI application
├── README.md
└── requirements.txt
```

## Setup

### 1. Create and activate virtual environment
```bash
python3 -m venv fastapi_lab1_env --without-pip
source fastapi_lab1_env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
rm get-pip.py
```

### 2. Install dependencies
```bash
fastapi_lab1_env/bin/pip install "fastapi[all]" scikit-learn numpy
```

## Usage

### 1. Train the model
```bash
cd src
python3 train.py
cd ..
```

### 2. Start the API server
```bash
python3 -m uvicorn src.main:app --reload
```

### 3. Access the API
- Swagger UI (interactive docs): http://localhost:8000/docs
- Health check: http://localhost:8000/

## API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | /          | Health check                       |
| POST   | /predict   | Predict malignant or benign tumor  |

### POST /predict

**Request Body:**
```json
{
  "mean_radius": 17.99,
  "mean_texture": 10.38,
  "mean_perimeter": 122.8,
  "mean_area": 1001.0,
  "mean_smoothness": 0.1184,
  "mean_compactness": 0.2776,
  "mean_concavity": 0.3001,
  "mean_concave_points": 0.1471,
  "mean_symmetry": 0.2419,
  "mean_fractal_dimension": 0.07871
}
```

**Response:**
```json
{
  "prediction": 0,
  "label": "malignant"
}
```

- `prediction`: 0 = malignant, 1 = benign
- `label`: human-readable classification result

## Testing
Visit http://localhost:8000/docs for the interactive Swagger UI. Click on **POST /predict → Try it out → fill the request body → Execute**.
```

---

