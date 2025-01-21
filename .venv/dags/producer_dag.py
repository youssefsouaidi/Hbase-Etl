from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'kafka_producer_dag',
    default_args=default_args,
    description='Run Kafka Producer every 5 minutes',
    schedule_interval=timedelta(seconds=10),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    run_producer = BashOperator(
        task_id='run_kafka_producer',
        bash_command='python C:\\Users\\Souai\\PycharmProjects\\ETL-hbase\\.venv\\prod.py',
        env={'PYTHONPATH': 'C:\\Users\\Souai\\PycharmProjects\\ETL-hbase'},
    )
