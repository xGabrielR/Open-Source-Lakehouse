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

    df_yellow_daily_descriptive = spark.sql("""
       WITH features AS (
        SELECT
            pickup_borough,
            dropoff_borough,
            payment_type,
            CAST(pickup_datetime AS DATE) AS pickup_date,
            CAST(dropoff_datetime AS DATE) AS dropoff_date,          
            ROUND((UNIX_TIMESTAMP(dropoff_datetime) - UNIX_TIMESTAMP(pickup_datetime)) / 60, 3) AS pd_seconds,
            passenger_count,
            trip_distance,
            tip_amount,
            extra,
            fare_amount,
            total_amount
        FROM iceberg.silver.yellow_trip
        WHERE pickup_datetime >= '2024-01-01'
        AND tip_amount >= 0
        AND total_amount >= 0
        AND extra >= 0
        AND fare_amount >= 0
    ),
    agg_features AS (
        SELECT 
            pickup_date,
            pickup_borough,
            MIN(pd_seconds) AS min_pd_seconds,
            MAX(pd_seconds) AS max_pd_seconds,
            AVG(pd_seconds) AS avg_pd_seconds,
            MIN(passenger_count) AS min_passenger_count,
            MAX(passenger_count) AS max_passenger_count,
            AVG(passenger_count) AS avg_passenger_count,
            MIN(trip_distance) AS min_trip_distance,
            MAX(trip_distance) AS max_trip_distance,
            AVG(trip_distance) AS avg_trip_distance,
            MIN(tip_amount) AS min_tip_amount,
            MAX(tip_amount) AS max_tip_amount,
            AVG(tip_amount) AS avg_tip_amount,
            MIN(extra) AS min_extra,
            MAX(extra) AS max_extra,
            AVG(extra) AS avg_extra,
            MIN(fare_amount) AS min_fare_amount,
            MAX(fare_amount) AS max_fare_amount,
            AVG(fare_amount) AS avg_fare_amount,
            MIN(total_amount) AS min_total_amount,
            MAX(total_amount) AS max_total_amount,
            AVG(total_amount) AS avg_total_amount,
            COUNT(DISTINCT CASE WHEN payment_type = 'Cash' THEN payment_type END) / COUNT(DISTINCT payment_type) AS pct_payment_cash,
            COUNT(DISTINCT CASE WHEN payment_type = 'Dispute' THEN payment_type END) / COUNT(DISTINCT payment_type) AS pct_payment_dispute,
            COUNT(DISTINCT CASE WHEN payment_type = 'No charge' THEN payment_type END) / COUNT(DISTINCT payment_type) AS pct_payment_no,
            COUNT(DISTINCT CASE WHEN payment_type = 'Credit card' THEN payment_type END) / COUNT(DISTINCT payment_type) AS pct_payment_credit,
            COUNT(DISTINCT CASE WHEN payment_type = 'Unknown' THEN payment_type END) / COUNT(DISTINCT payment_type) AS pct_payment_unknown
        FROM features
        GROUP BY pickup_date, pickup_borough
    )
    SELECT
        *
    FROM agg_features
    """)

    write_iceberg_table(
        df_yellow_daily_descriptive,
        table_name="yellow_daily_descriptive",
        catalog_name=CATALOG_NAME,
        schema_name=GOLD_SCHEMA_NAME,
        bucket_name=GOLD_BUCKET
    )