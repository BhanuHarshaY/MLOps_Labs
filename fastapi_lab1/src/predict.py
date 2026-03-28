import pickle
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/cancer_model.pkl")

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

def run_prediction(features: list) -> dict:
    model = load_model()
    input_array = np.array(features).reshape(1, -1)
    prediction = int(model.predict(input_array)[0])
    label = "benign" if prediction == 1 else "malignant"
    return {"prediction": prediction, "label": label}