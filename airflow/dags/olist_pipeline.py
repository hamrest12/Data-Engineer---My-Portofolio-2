
from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/dbt/olist_dbt"
PROFILES_DIR = PROJECT_DIR


@dag(
    dag_id="olist_data_pipeline",
    description="Olist pipeline: Bronze to Silver to Gold",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["olist", "clickhouse", "dbt"],
)
def olist_pipeline():

    @task.bash
    def load_bronze():
        return """
        python /opt/airflow/scripts/04_load_bronze.py
        """

    dbt_silver = BashOperator(
        task_id="dbt_silver",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"dbt run --select silver "
            f"--profiles-dir {PROFILES_DIR}"
        ),
    )

    dbt_gold = BashOperator(
        task_id="dbt_gold",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"dbt run --select gold "
            f"--profiles-dir {PROFILES_DIR}"
        ),
    )

    bronze_task = load_bronze()

    bronze_task >> dbt_silver >> dbt_gold


olist_pipeline()
