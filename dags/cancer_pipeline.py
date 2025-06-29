from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.load_data import load_dataset
from etl.preprocess import preprocess_data
from etl.train_model import train_model
from etl.evaluate import evaluate_model
from etl.save_results import save_artifacts
from datetime import timedelta

def notify_failure(context):
    task_id = context['task_instance'].task_id
    dag_id = context['task_instance'].dag_id
    print(f"Task {task_id} in DAG {dag_id} failed!")

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': notify_failure
}

with DAG(
    'breast_cancer_pipeline',
    default_args=default_args,
    description='ETL pipeline for breast cancer diagnosis',
    schedule='@daily',  # Используйте 'schedule' вместо 'schedule_interval'
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['medical']
) as dag:

    # Определяем задачи без явных зависимостей
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_dataset
    )

    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
        op_kwargs={'df': "{{ ti.xcom_pull(task_ids='load_data') }}"}
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        op_kwargs={
            'X_train': "{{ ti.xcom_pull(task_ids='preprocess_data')['X_train'] }}",
            'y_train': "{{ ti.xcom_pull(task_ids='preprocess_data')['y_train'] }}"
        }
    )

    evaluate_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
        op_kwargs={
            'model': "{{ ti.xcom_pull(task_ids='train_model') }}",
            'X_test': "{{ ti.xcom_pull(task_ids='preprocess_data')['X_test'] }}",
            'y_test': "{{ ti.xcom_pull(task_ids='preprocess_data')['y_test'] }}"
        }
    )

    save_task = PythonOperator(
        task_id='save_results',
        python_callable=save_artifacts,
        op_kwargs={
            'model': "{{ ti.xcom_pull(task_ids='train_model') }}",
            'metrics': "{{ ti.xcom_pull(task_ids='evaluate_model') }}"
        }
    )

    load_task >> preprocess_task >> train_task >> evaluate_task >> save_task