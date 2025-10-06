# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.lab import (
    load_data,
    data_preprocessing,
    build_save_model,
    load_model_elbow,
    visualize_clusters,   # NEW: include the visualizer
)

# Note:
# In Airflow 3.x, enabling XCom pickling should be done via environment variable:
# export AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
# The old airflow.configuration API is deprecated.

# Define default arguments for your DAG
default_args = {
    'owner': 'akshaj',
    'start_date': datetime(2025, 10, 5),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Create a DAG instance
dag = DAG(
    dag_id='Airflow_Lab1',
    default_args=default_args,
    description='Your Python DAG Description',
    schedule_interval=None,  # manual trigger; change if you want it scheduled
    catchup=False,
)

# Task 1 - Load data
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag,
)

# Task 2 - Preprocess
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],   # XCom from previous task
    dag=dag,
)

# Task 3 - Build & save model
build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, "model2.sav"],
    dag=dag,
)

# Task 4 - Load model & compute elbow + sample prediction string
load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_elbow,
    op_args=["model2.sav", build_save_model_task.output],  # filename + SSE list
    dag=dag,
)

# Task 5 - Visualize clusters using the saved model
visualize_clusters_task = PythonOperator(
    task_id='visualize_clusters_task',
    python_callable=visualize_clusters,
    op_args=["model2.sav"],
    dag=dag,
)

#  Task dependencies
load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task
build_save_model_task >> visualize_clusters_task  # visualize after model is saved

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
