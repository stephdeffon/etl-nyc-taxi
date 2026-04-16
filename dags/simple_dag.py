from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def hello():
    print("Hello Airflow 🚀")


with DAG(
    dag_id="hello_world_3",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # manuel
    catchup=False
) as dag:

    hello_task = PythonOperator(
        task_id="say_hello_3",
        python_callable=hello
    )