from pyspark.sql import SparkSession
from pyspark.sql import functions as pf

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
    df_location = spark.table("iceberg.bronze.location").select(
        pf.col("LocationID").alias("location_id"),
        pf.col("Borough").alias("borough"),
        pf.col("Zone").alias("zone"),
    )

    df_location = pf.broadcast(df_location)

    df_yellow_trip = spark.table("iceberg.bronze.yellow_trip").select(
        pf.col("VendorID").alias("vendor_id"),
        pf.col("PULocationID").alias("pickup_location_id"),
        pf.col("DOLocationID").alias("dropoff_location_id"),
        pf.to_timestamp(pf.col("tpep_pickup_datetime")).alias("pickup_datetime"),
        pf.to_timestamp(pf.col("tpep_dropoff_datetime")).alias("dropoff_datetime"),
        pf.when(
            pf.col("payment_type") == 1, "Credit card").when(
            pf.col("payment_type") == 2, "Cash").when(
            pf.col("payment_type") == 3, "No charge").when(
            pf.col("payment_type") == 4, "Dispute").when(
            pf.col("payment_type") == 6, "Voided trip"
        ).otherwise("Unknown").alias("payment_type"),
        pf.col("passenger_count").alias("passenger_count"),
        pf.col("trip_distance").alias("trip_distance"),
        pf.col("fare_amount").alias("fare_amount"),
        pf.col("extra").alias("extra"),
        pf.col("tip_amount").alias("tip_amount"),
        pf.col("total_amount").alias("total_amount"),
        pf.col("congestion_surcharge").alias("congestion_surcharge")
    )

    df_yellow_trip = df_yellow_trip.join(
        df_location.select(
            pf.col("location_id").alias("pickup_location_id"),
            pf.col("borough").alias("pickup_borough"),
            pf.col("zone").alias("pickup_zone")
        ),
        on="pickup_location_id",
        how="left"
    ).join(
        df_location.select(
            pf.col("location_id").alias("dropoff_location_id"),
            pf.col("borough").alias("dropoff_borough"),
            pf.col("zone").alias("dropoff_zone")
        ),
        on="dropoff_location_id",
        how="left"
    ).drop(*["dropoff_location_id", "pickup_location_id"])

    write_iceberg_table(
        df_yellow_trip,
        table_name="yellow_trip",
        catalog_name=CATALOG_NAME,
        schema_name=SILVER_SCHEMA_NAME,
        bucket_name=SILVER_BUCKET
    )