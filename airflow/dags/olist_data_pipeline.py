import pendulum
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# Lokasi project di dalam container Airflow
PROJECT_DIR = "/opt/airflow/dbt/olist_dbt"
PROFILES_DIR = "/opt/airflow/dbt/olist_dbt"
BRONZE_SCRIPT = "/opt/airflow/scripts/04_load_bronze.py"

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="olist_data_pipeline",
    description="Olist Bronze to Silver to Gold Pipeline",
    default_args=default_args,
    start_date=pendulum.datetime(
        2026, 1, 1,
        tz="Asia/Jakarta"
    ),
    schedule="0 0 * * *",
    catchup=False,
    tags=["olist", "clickhouse", "dbt"],
) as dag:

    # Task 1: Load CSV files into Bronze
    load_bronze = BashOperator(
        task_id="load_bronze",
        bash_command=f"python {BRONZE_SCRIPT}",
    )

    # Task 2: Transform Bronze into Silver
    dbt_silver = BashOperator(
        task_id="dbt_silver",
        bash_command=(
            f"dbt run "
            f"--project-dir {PROJECT_DIR} "
            f"--profiles-dir {PROFILES_DIR} "
            f"--select silver"
        ),
    )

    # Task 3: Transform Silver into Gold
    dbt_gold = BashOperator(
        task_id="dbt_gold",
        bash_command=(
            f"dbt run "
            f"--project-dir {PROJECT_DIR} "
            f"--profiles-dir {PROFILES_DIR} "
            f"--select gold"
        ),
    )

    # Task dependencies
    load_bronze >> dbt_silver >> dbt_gold
