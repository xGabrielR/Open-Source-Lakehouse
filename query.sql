-- Create Minio Laning schema
CREATE SCHEMA minio.landing
WITH (location = 's3://grc-lh-landing/')

-- Yellow Taxi data from Landing into Trino
CREATE TABLE IF NOT EXISTS minio.landing.yellow_trip (
    VendorID integer,
    tpep_pickup_datetime timestamp,
    tpep_dropoff_datetime timestamp,
    passenger_count integer,
    trip_distance double,
    RatecodeID integer,
    store_and_fwd_flag varchar,
    PULocationID integer,
    DOLocationID integer,
    payment_type integer,
    fare_amount double,
    extra double,
    mta_tax double,
    tip_amount double,
    tolls_amount double,
    improvement_surcharge double,
    total_amount double,
    congestion_surcharge double,
    Airport_fee double
)
WITH (
  format = 'PARQUET',
  external_location = 's3a://grc-lh-landing/taxi/yellow_trip'
);

SELECT * FROM minio.landing.yellow_trip LIMIT 5;

-- Create Lakehouse Schemas
CREATE SCHEMA IF NOT EXISTS nessie.bronze with (location = 's3a://grc-lh-bronze/');
CREATE SCHEMA IF NOT EXISTS nessie.silver with (location = 's3a://grc-lh-silver/');
CREATE SCHEMA IF NOT EXISTS nessie.gold with (location = 's3a://grc-lh-gold/');

-- Create iceberg table with Trino
CREATE TABLE IF NOT EXISTS nessie.bronze.retail (
	customerid bigint,
	invoiceno bigint,
	stockcode varchar
)
WITH (
	format = 'PARQUET',
	location = 's3a://grc-lh-bronze/bronze.db/retail'
);

-- Query Gold Table
SELECT * FROM nessie.gold.yellow_daily_descriptive
ORDER BY pickup_date DESC;
