from pyspark.sql import SparkSession

# I can provide arguments as input inside spark-submit
LANDING_PREFIX = "taxi"
LANDING_BUCKET = "grc-lh-landing"
BRONZE_BUCKET = "grc-lh-bronze"
SILVER_BUCKET = "grc-lh-silver"
GOLD_BUCKET = "grc-lh-gold"

CATALOG_NAME = "iceberg"
BRONZE_SCHEMA_NAME = "bronze"
SILVER_SCHEMA_NAME = "silver"
GOLD_SCHEMA_NAME = "gold"

def write_iceberg_table(
    df,
    table_name: str,
    catalog_name: str,
    schema_name: str,
    bucket_name: str
) -> None:
    df.coalesce(1).writeTo(f"{catalog_name}.{schema_name}.{table_name}") \
        .using("iceberg") \
        .tableProperty("location", f"s3a://{bucket_name}/{schema_name}.db/{table_name}") \
        .tableProperty("write.format.default", "parquet") \
        .tableProperty("write.distribution-mode", "hash") \
        .tableProperty("write.parquet.dict-size-bytes", "134217728") \
        .createOrReplace()

if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()

    # Read & Write Data
    df_location = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(f"s3a://{LANDING_BUCKET}/{LANDING_PREFIX}/location")
    df_yellow_tip = spark.read.format("parquet").load(f"s3a://{LANDING_BUCKET}/{LANDING_PREFIX}/yellow_trip")

    write_iceberg_table(
        df_location,
        table_name="location",
        catalog_name=CATALOG_NAME,
        schema_name=BRONZE_SCHEMA_NAME,
        bucket_name=BRONZE_BUCKET
    )

    write_iceberg_table(
        df_yellow_tip,
        table_name="yellow_trip",
        catalog_name=CATALOG_NAME,
        schema_name=BRONZE_SCHEMA_NAME,
        bucket_name=BRONZE_BUCKET
    )