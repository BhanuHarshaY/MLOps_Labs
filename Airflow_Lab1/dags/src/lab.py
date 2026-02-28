"""
lab.py - Mall Customer Segmentation using K-Means Clustering
MLOps Airflow Lab 1 - Original Implementation
"""

import os
import pickle
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'file.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data():
    """
    Load mall customer data from CSV file.
    Selects the numeric features relevant for clustering and serializes the DataFrame.

    Returns:
        bytes: Pickled DataFrame with selected features.
    """
    logger.info("Loading data from: %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH)

    # Select numeric features for clustering
    features = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
    logger.info("Loaded %d records with features: %s", len(features), list(features.columns))

    return pickle.dumps(features)


def data_preprocessing(serialized_data):
    """
    Deserialize data, handle missing values, and apply StandardScaler normalization.

    Args:
        serialized_data (bytes): Pickled DataFrame from load_data().

    Returns:
        bytes: Pickled scaled numpy array ready for clustering.
    """
    logger.info("Starting data preprocessing...")
    df = pickle.loads(serialized_data)

    # Drop rows with missing values
    initial_count = len(df)
    df = df.dropna()
    logger.info("Dropped %d rows with missing values. Remaining: %d", initial_count - len(df), len(df))

    # Standardize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    logger.info("Features standardized. Shape: %s", scaled_data.shape)

    return pickle.dumps(scaled_data)


def build_save_model(serialized_data, filename):
    """
    Build K-Means models for k=1 to 10, compute SSE for each,
    and save the best model (k=5) to disk.

    Args:
        serialized_data (bytes): Pickled scaled array from data_preprocessing().
        filename (str): Filename to save the model (e.g., 'model.sav').

    Returns:
        bytes: Pickled list of SSE values for k=1 to 10.
    """
    logger.info("Building K-Means models to evaluate optimal clusters...")
    scaled_data = pickle.loads(serialized_data)

    sse_values = []
    k_range = range(1, 11)

    for k in k_range:
        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        kmeans.fit(scaled_data)
        sse_values.append(kmeans.inertia_)
        logger.info("k=%d | SSE=%.2f", k, kmeans.inertia_)

    # Save the model with k=5 as the candidate model
    best_k = 5
    final_model = KMeans(n_clusters=best_k, init='k-means++', n_init=10, random_state=42)
    final_model.fit(scaled_data)

    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, 'wb') as f:
        pickle.dump(final_model, f)

    logger.info("Model saved to: %s", model_path)
    return pickle.dumps(sse_values)


def load_model_elbow(filename, serialized_sse):
    """
    Load a saved K-Means model and determine the optimal number of clusters
    using the elbow method via the KneeLocator library.

    Args:
        filename (str): Filename of the saved model (e.g., 'model.sav').
        serialized_sse (bytes): Pickled SSE values list from build_save_model().

    Returns:
        str: A message stating the optimal number of clusters.
    """
    logger.info("Loading saved model and applying elbow method...")
    sse_values = pickle.loads(serialized_sse)

    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    logger.info("Model loaded. It was trained with k=%d clusters.", model.n_clusters)

    # Apply elbow method
    k_range = list(range(1, 11))
    kneedle = KneeLocator(k_range, sse_values, curve='convex', direction='decreasing')
    optimal_k = kneedle.elbow

    if optimal_k is None:
        result = "Elbow point not detected. Consider reviewing the SSE plot."
    else:
        result = f"Optimal number of clusters (Elbow Method): {optimal_k}"

    logger.info(result)
    logger.info("SSE values: %s", [round(v, 2) for v in sse_values])
    return result
