-- Active: 1768146676801@@127.0.0.1@5432@postgres
CREATE SCHEMA IF NOT EXISTS "dwh";


CREATE TABLE IF NOT EXISTS "dwh".fact_trips(
    trip_id SERIAL PRIMARY KEY,
    tpep_pickup_datetime TIMESTAMP,
    tpep_drop_off_datetime TIMESTAMP,
    passenger_count int,
    pu_locationID int,
    do_LocationID int,
    fare_amount int,
    tip_amount int,
    trip_duration int,
    pickup_date date,
    pickup_time time,
    pickhup_hour int,
    dwh_create_date timestamp DEFAULT current_date
)