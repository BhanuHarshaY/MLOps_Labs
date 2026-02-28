"""
airflow.py - Airflow DAG for Mall Customer Segmentation
MLOps Airflow Lab 1 - Original Implementation

DAG: MallCustomer_Clustering
Pipeline: load_data -> data_preprocessing -> build_save_model -> load_model_elbow
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow
from airflow import configuration as conf

# Enable pickle support for XCom so data can be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

# Default arguments for the DAG
default_args = {
    'owner': 'bhanu_harsha',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG instance
dag = DAG(
    'MallCustomer_Clustering',
    default_args=default_args,
    description='K-Means clustering pipeline on Mall Customer dataset using the Elbow Method',
    schedule_interval=None,   # Manual trigger only
    catchup=False,
)

# Task 1: Load data from CSV
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag,
)

# Task 2: Preprocess the loaded data
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)

# Task 3: Build K-Means models and save the best one
build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, 'model.sav'],
    provide_context=True,
    dag=dag,
)

# Task 4: Load saved model and determine optimal clusters via elbow method
load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_elbow,
    op_args=['model.sav', build_save_model_task.output],
    dag=dag,
)

# Define task execution order
load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task

# Allow CLI interaction when run directly
if __name__ == "__main__":
    dag.cli()
