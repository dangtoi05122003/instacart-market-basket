from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
default_args = {
    'owner': "bronze",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
with DAG (
    dag_id = "medallion",
    default_args = default_args,
    start_date = datetime(2025, 5, 5),
    schedule_interval = '@daily',
    catchup = False,
    max_active_runs = 1
) as dag:
    task_1 = BashOperator(
        task_id = 'bronze',
        bash_command = 'python /opt/airflow/src/ingestion/bronze.py'
    )
    task_2 = BashOperator (
        task_id = "silver",
        bash_command = "python /opt/airflow/src/transform/silver.py"
    )
    task_3 = BashOperator(
        task_id = 'gold',
        bash_command = 'python /opt/airflow/src/transform/gold.py'  
    )
    task_1 >> task_2 >> task_3