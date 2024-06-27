from docker import APIClient
from functools import cached_property

from airflow.models import Variable
from airflow.models import BaseOperator
from airflow.providers.docker.hooks.docker import DockerHook

class SparkSubmitDockerOperator(BaseOperator):
    def __init__(
        self,
        spark_job_name: str,
        api_version: str = "auto",
        timeout: int = 60,
        docker_url: str = Variable.get("docker_url"),
        spark_cluster_container_id: str = Variable.get("spark_cluster_id"),
        docker_conn_id: str | bool = None, # TODO: Add docker_default instead of overwrting
        **kwargs
    ):
        super().__init__(**kwargs)
        self.docker_url = docker_url
        self.api_version = api_version
        self.timeout = timeout
        self.spark_job_name = spark_job_name
        self.docker_conn_id = docker_conn_id
        self.spark_cluster_container_id = spark_cluster_container_id

    @cached_property
    def hook(self) -> DockerHook:
        return DockerHook(
            base_url=self.docker_url,
            version=self.api_version,
            timeout=self.timeout,
            docker_conn_id=self.docker_conn_id
        )
    
    @property
    def cli(self) -> APIClient:
        return self.hook.api_client

    def execute(self, context):
        self.log.info("Executing SparkSubmitDockerOperator")
        
        deploy_mode = "--deploy-mode client"
        extra_spark_confs = "--conf spark.sql.catalog.iceberg.warehouse=s3a://warehouse/iceberg/"
        command = f"spark-submit --master spark://spark-master:7077 {deploy_mode} --name {self.spark_job_name} {extra_spark_confs} s3a://grc-lh-scripts/spark_jobs/{self.spark_job_name}.py"
        
        exec_id = self.cli.exec_create(self.spark_cluster_container_id, command)["Id"]
        spark_cluster_container_output = self.cli.exec_start(exec_id)

        self.log.info(spark_cluster_container_output)