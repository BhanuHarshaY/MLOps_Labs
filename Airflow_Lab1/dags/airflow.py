"""
airflow.py - Airflow DAG for Mall Customer Segmentation
MLOps Airflow Lab 1 - Original Implementation

DAG: MallCustomer_Clustering
Pipeline:
    load_data -> data_preprocessing -> build_save_model
    -> load_model_elbow (+ elbow plot) -> generate_report
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow, generate_report
from airflow import configuration as conf

# Enable pickle support for XCom so data can be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

default_args = {
    'owner': 'bhanu_harsha',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'MallCustomer_Clustering',
    default_args=default_args,
    description='K-Means clustering pipeline on Mall Customer dataset with elbow plot and cluster report',
    schedule_interval=None,
    catchup=False,
)

load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag,
)

data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)

build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, 'model.sav'],
    provide_context=True,
    dag=dag,
)

load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_elbow,
    op_args=[build_save_model_task.output, data_preprocessing_task.output],
    dag=dag,
)

generate_report_task = PythonOperator(
    task_id='generate_report_task',
    python_callable=generate_report,
    op_args=[load_model_task.output, data_preprocessing_task.output],
    dag=dag,
)

# Task execution order
load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task >> generate_report_task

if __name__ == "__main__":
    dag.cli()