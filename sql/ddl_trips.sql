-- Active: 1768146676801@@127.0.0.1@5432@postgres
CREATE SCHEMA IF NOT EXISTS "dwh";


CREATE TABLE IF NOT EXISTS "dwh".fact_trips(
    trip_id SERIAL PRIMARY KEY,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count int,
    pu_location_id int,
    do_location_id int,
    fare_amount int,
    tip_amount int,
    trip_duration int,
    pickup_date date,
    pickup_time time,
    pickup_hour int,
    dropoff_date date,
    dropoff_time time,
    dropoff_hour int,
    source_month int,
    source_year int,
    dwh_create_date timestamp DEFAULT current_date
)
