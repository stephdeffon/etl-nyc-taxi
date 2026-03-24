
from fileinput import filename

from src.extract_trips import fetch_taxi_trip_file
from src.transform_trips import transform_trips
from src.load_trips import init_trips, load_trips, delete_existing_month
from src.config import log
import argparse

import pendulum

from airflow.decorators import dag, task

month_param = '02'
year_param='2025'
force=False

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['example'],
)
def nyc_trips_etl():

    @task()
    def extract(month,year,force):
        print('start extract')
        filename = fetch_taxi_trip_file(month, year, force)
        return str(filename)
    
    @task()
    def transform(filename,month,year):
        #transform
        df = transform_trips(Path(filename),month,year)
        path = str(DATA_DIR) + f'/silver/tripdata_{month}_{year}.parquet'
        df.to_parquet(path)

        return path
    @task()
    def init_trips_task():
        print('init')
        init_trips()

    @task()
    def delete_existing_month_task(month,year):
        print('start delete')
        deleted_rows = delete_existing_month(month,year)
        return deleted_rows
    
    @task()
    def load(df_path):
        import pandas as pd
        df=pd.read_parquet(df_path)
        inserted_rows=load_trips(df)
        return inserted_rows
    
    filename=extract(month_param,year_param,force)
    df=transform(filename,month_param,year_param)
    init_trips_task()
    del_rows = delete_existing_month_task(month_param,year_param)
    ins_rows = load(df)

nyc_trips_dag = nyc_trips_etl()