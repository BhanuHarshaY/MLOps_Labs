import sys
import os

from fastapi import FastAPI, HTTPException
from src.data import CancerData, CancerResponse
from src.predict import run_prediction

app = FastAPI(
    title="Breast Cancer Prediction API",
    description="Predicts whether a tumor is benign or malignant using a Random Forest Classifier.",
    version="1.0.0"
)

@app.get("/")
async def health_ping():
    return {"status": "ok", "message": "Breast Cancer Prediction API is running"}

@app.post("/predict", response_model=CancerResponse)
async def predict_cancer(data: CancerData):
    try:
        features = [
            data.mean_radius,
            data.mean_texture,
            data.mean_perimeter,
            data.mean_area,
            data.mean_smoothness,
            data.mean_compactness,
            data.mean_concavity,
            data.mean_concave_points,
            data.mean_symmetry,
            data.mean_fractal_dimension
        ]
        result = run_prediction(features)
        return CancerResponse(
            prediction=result["prediction"],
            label=result["label"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))