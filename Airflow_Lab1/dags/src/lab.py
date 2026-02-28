"""
lab.py - Mall Customer Segmentation using K-Means Clustering
MLOps Airflow Lab 1 - Original Implementation

Pipeline:
    load_data -> data_preprocessing -> build_save_model
    -> load_model_elbow (+ elbow plot) -> generate_report
"""

import os
import pickle
import logging
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'file.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')

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

    features = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
    features = features.rename(columns={
        'Annual Income (k$)': 'Annual_Income',
        'Spending Score (1-100)': 'Spending_Score'
    })

    logger.info("Loaded %d records with features: %s", len(features), list(features.columns))
    return pickle.dumps(features)


def data_preprocessing(serialized_data):
    """
    Deserialize data, handle missing values, and apply StandardScaler normalization.

    Args:
        serialized_data (bytes): Pickled DataFrame from load_data().

    Returns:
        bytes: Pickled dict with scaled array and original DataFrame.
    """
    logger.info("Starting data preprocessing...")
    df = pickle.loads(serialized_data)

    initial_count = len(df)
    df = df.dropna()
    logger.info("Dropped %d rows with missing values. Remaining: %d", initial_count - len(df), len(df))

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    logger.info("Features standardized. Shape: %s", scaled_data.shape)

    payload = {
        'scaled': scaled_data,
        'original': df
    }
    return pickle.dumps(payload)


def build_save_model(serialized_data, filename):
    """
    Build K-Means models for k=1 to 10, compute SSE for each,
    and save the best candidate model to disk.

    Args:
        serialized_data (bytes): Pickled payload dict from data_preprocessing().
        filename (str): Filename to save the model (e.g., 'model.sav').

    Returns:
        bytes: Pickled dict with SSE values and filename.
    """
    logger.info("Building K-Means models to evaluate optimal clusters...")
    payload = pickle.loads(serialized_data)
    scaled_data = payload['scaled']

    sse_values = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        kmeans.fit(scaled_data)
        sse_values.append(kmeans.inertia_)
        logger.info("k=%d | SSE=%.2f", k, kmeans.inertia_)

    best_k = 5
    final_model = KMeans(n_clusters=best_k, init='k-means++', n_init=10, random_state=42)
    final_model.fit(scaled_data)

    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, 'wb') as f:
        pickle.dump(final_model, f)

    logger.info("Model saved to: %s", model_path)
    return pickle.dumps({'sse_values': sse_values, 'filename': filename})


def load_model_elbow(serialized_model_data, serialized_preprocessed):
    """
    Load a saved K-Means model, determine the optimal number of clusters
    using the elbow method, and save the elbow curve plot to dags/outputs/.

    Args:
        serialized_model_data (bytes): Pickled dict from build_save_model().
        serialized_preprocessed (bytes): Pickled payload dict from data_preprocessing().

    Returns:
        bytes: Pickled dict with optimal_k, sse_values, and plot path.
    """
    logger.info("Loading saved model and applying elbow method...")
    model_data = pickle.loads(serialized_model_data)
    sse_values = model_data['sse_values']
    filename = model_data['filename']

    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    logger.info("Model loaded. It was trained with k=%d clusters.", model.n_clusters)

    k_range = list(range(1, 11))
    kneedle = KneeLocator(k_range, sse_values, curve='convex', direction='decreasing')
    optimal_k = kneedle.elbow

    if optimal_k is None:
        logger.warning("Elbow point not detected. Defaulting to k=5.")
        optimal_k = 5

    logger.info("Optimal number of clusters (Elbow Method): %d", optimal_k)
    logger.info("SSE values: %s", [round(v, 2) for v in sse_values])

    # Plot and save elbow curve
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plot_path = os.path.join(OUTPUT_DIR, 'elbow_curve.png')

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(k_range, sse_values, marker='o', linewidth=2,
            color='steelblue', markersize=7, label='SSE per k')
    ax.axvline(x=optimal_k, color='crimson', linestyle='--',
               linewidth=2, label=f'Optimal k = {optimal_k}')
    ax.scatter([optimal_k], [sse_values[optimal_k - 1]],
               color='crimson', s=120, zorder=5)
    ax.set_title('Elbow Method — Optimal Number of Clusters', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Clusters (k)', fontsize=12)
    ax.set_ylabel('Sum of Squared Errors (SSE)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()

    logger.info("Elbow curve saved to: %s", plot_path)

    return pickle.dumps({
        'optimal_k': optimal_k,
        'sse_values': sse_values,
        'plot_path': plot_path
    })


def generate_report(serialized_elbow_data, serialized_preprocessed):
    """
    Fit the final K-Means model using optimal_k, assign cluster labels,
    and log a summary report with per-cluster statistics.

    Args:
        serialized_elbow_data (bytes): Pickled dict from load_model_elbow().
        serialized_preprocessed (bytes): Pickled payload dict from data_preprocessing().

    Returns:
        str: Summary report as a string.
    """
    logger.info("Generating cluster summary report...")

    elbow_data = pickle.loads(serialized_elbow_data)
    preprocessed = pickle.loads(serialized_preprocessed)

    optimal_k = elbow_data['optimal_k']
    scaled_data = preprocessed['scaled']
    original_df = preprocessed['original']

    final_model = KMeans(n_clusters=optimal_k, init='k-means++', n_init=10, random_state=42)
    labels = final_model.fit_predict(scaled_data)
    original_df = original_df.copy()
    original_df['Cluster'] = labels

    report_lines = []
    report_lines.append("=" * 55)
    report_lines.append("   MALL CUSTOMER SEGMENTATION — CLUSTER REPORT")
    report_lines.append("=" * 55)
    report_lines.append(f"  Optimal k (Elbow Method) : {optimal_k}")
    report_lines.append(f"  Total customers          : {len(original_df)}")
    report_lines.append("=" * 55)

    for cluster_id in range(optimal_k):
        cluster_df = original_df[original_df['Cluster'] == cluster_id]
        report_lines.append(f"\n  Cluster {cluster_id}  ({len(cluster_df)} customers)")
        report_lines.append(f"    Avg Age            : {cluster_df['Age'].mean():.1f}")
        report_lines.append(f"    Avg Annual Income  : ${cluster_df['Annual_Income'].mean():.1f}k")
        report_lines.append(f"    Avg Spending Score : {cluster_df['Spending_Score'].mean():.1f}")
        report_lines.append(f"    Age Range          : {cluster_df['Age'].min()} - {cluster_df['Age'].max()}")

    report_lines.append("\n" + "=" * 55)
    report_lines.append("  Elbow curve saved to: dags/outputs/elbow_curve.png")
    report_lines.append("=" * 55)

    report = "\n".join(report_lines)
    logger.info("\n%s", report)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_path = os.path.join(OUTPUT_DIR, 'cluster_report.txt')
    with open(report_path, 'w') as f:
        f.write(report)

    logger.info("Report saved to: %s", report_path)
    return report