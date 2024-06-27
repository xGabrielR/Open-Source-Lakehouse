# Open Source Lakehouse

---

Open Source Lakehouse repo for study.

![Architecture](./assets/architecture.png)

The main tool is Airflow for orchestration of Pyspark Lakehouse jobs.

![Airflow](./assets/airflow_yellow_trip.png)

With trino i can query in real time Landing in any available format (CSV and Parquet) and query Apache Iceberg tables from Nessie Catalog. 

![Trino](./assets/dbeaver_trino_query_gold_table.png)

The Minio Buckets is created with Terraform.

![Minio](./assets/minio_buckets.png)

Nessie is the Metadata Catalog for Apache Iceberg, is possible to change to Open Source Unity Catalog.

![Nessie](./assets/nessie_lakehouse_schemas.png)

![Commits](./assets/nessie_lakehouse_commits.png)

Next Steps:

1. Add Exploratory Notebook;
2. Add MLFLOW;
3. Create Machine Learning Pipeline for Trip Data;
4. Improve Custom Docker Submit.
