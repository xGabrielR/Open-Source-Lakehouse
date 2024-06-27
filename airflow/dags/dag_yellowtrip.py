from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from SparkExecOperator import SparkSubmitDockerOperator

from datetime import datetime, timedelta

DEFAULT_ARGS = {
    "start_date": datetime(2024, 1, 1)
}

@dag(
    description="Yellow Trip Taxi Workflow",
    tags=["yellow", "spark"],
    default_args=DEFAULT_ARGS,
    schedule_interval=timedelta(minutes=60),
    dagrun_timeout=timedelta(minutes=25),
    max_active_runs=2,
    catchup=False
)
def YELLOW_TRIP():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    submit_bronze = SparkSubmitDockerOperator(
        task_id="submit_bronze",
        docker_url="http://docker-socket-proxy:2375", # Docker Proxy URL
        spark_cluster_container_id="f1ce4efb35ce",    # Spark Cluster Docker Id
        spark_job_name="bronze_nyc_trip"
    )

    submit_silver = SparkSubmitDockerOperator(
        task_id="submit_silver",
        spark_job_name="silver_yellow_trip"
    )

    submit_gold = SparkSubmitDockerOperator(
        task_id="submit_gold",
        spark_job_name="gold_yellow_trip"
    )

    start >> submit_bronze >> submit_silver >> submit_gold >> end

YELLOW_TRIP()