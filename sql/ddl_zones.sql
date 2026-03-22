CREATE SCHEMA IF NOT EXISTS "dwh";


CREATE TABLE IF NOT EXISTS "dwh".dim_zones(
    location_id int PRIMARY KEY,
    borough varchar(50),
    zone varchar(50),
    service_zone VARCHAR(50),
    dwh_create_date timestamp DEFAULT current_date
)