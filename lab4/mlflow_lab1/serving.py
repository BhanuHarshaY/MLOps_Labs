"""
serving.py - MLflow Custom Artifacts

This script demonstrates creating custom artifacts with MLflow,
including extra_pip_requirements.txt for model reproducibility.

Dataset: California Housing (sklearn built-in)
Model: Decision Tree Regressor
"""

import mlflow
mlflow.set_tracking_uri("file:./mlruns")
import mlflow.sklearn
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import os
import json


def train_and_log_with_artifacts():
    """Train a model and log it with custom artifacts."""

    # Load data
    housing = fetch_california_housing()
    X = pd.DataFrame(housing.data, columns=housing.feature_names)
    y = housing.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Set experiment
    mlflow.set_experiment("california-housing-custom-artifacts")

    with mlflow.start_run(run_name="custom-artifacts-run") as run:
        # Train model
        model = DecisionTreeRegressor(
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=3,
            random_state=42,
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Log parameters
        mlflow.log_param("model_type", "DecisionTreeRegressor")
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("min_samples_split", 5)
        mlflow.log_param("min_samples_leaf", 3)
        mlflow.log_param("dataset", "california_housing")

        # Log metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2_score", r2)

        # Create and log custom artifacts 

        # 1. Create extra_pip_requirements.txt
        pip_requirements = [
            "scikit-learn==1.8.0",
            "pandas==2.3.3",
            "numpy==2.4.3",
        ]
        with open("extra_pip_requirements.txt", "w") as f:
            f.write("\n".join(pip_requirements))
        mlflow.log_artifact("extra_pip_requirements.txt")

        # 2. Create a model summary JSON
        model_summary = {
            "model_type": "DecisionTreeRegressor",
            "dataset": "California Housing",
            "n_features": X_train.shape[1],
            "n_train_samples": X_train.shape[0],
            "n_test_samples": X_test.shape[0],
            "feature_names": list(housing.feature_names),
            "metrics": {"mse": round(mse, 4), "r2_score": round(r2, 4)},
            "hyperparameters": {
                "max_depth": 10,
                "min_samples_split": 5,
                "min_samples_leaf": 3,
                "random_state": 42,
            },
        }
        with open("model_summary.json", "w") as f:
            json.dump(model_summary, f, indent=2)
        mlflow.log_artifact("model_summary.json")

        # 3. Create feature importance artifact
        feature_importance = pd.DataFrame(
            {
                "feature": housing.feature_names,
                "importance": model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        feature_importance.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")

        # 4. Log the model with extra pip requirements
        mlflow.sklearn.log_model(
            model,
            "decision-tree-model",
            extra_pip_requirements=pip_requirements,
        )

        # Print results
        print(f"\n{'='*50}")
        print(f"Run ID: {run.info.run_id}")
        print(f"MSE: {mse:.4f}")
        print(f"R2 Score: {r2:.4f}")
        print(f"{'='*50}")
        print(f"\nCustom artifacts logged:")
        print(f"  - extra_pip_requirements.txt")
        print(f"  - model_summary.json")
        print(f"  - feature_importance.csv")
        print(f"\nFeature Importance:")
        print(feature_importance.to_string(index=False))
        print(f"\nRun 'mlflow ui --port 5001' to view artifacts in the UI.")

    # Clean up local artifact files
    for f in [
        "extra_pip_requirements.txt",
        "model_summary.json",
        "feature_importance.csv",
    ]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    train_and_log_with_artifacts()
