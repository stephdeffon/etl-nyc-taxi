import pendulum

from airflow.sdk import dag, task


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["etl_trip"],
    params={
        "month": "02",
        "year": "2025",
        "force": False,
    },
)
def nyc_trips_etl():

    @task()
    def extract(**context):
        from src.extract_trips import fetch_taxi_trip_file

        month = context["params"]["month"]
        year = context["params"]["year"]
        force = context["params"]["force"]
        print("start extract")
        filename = fetch_taxi_trip_file(month, year, force)
        return str(filename)

    @task()
    def transform(filename, **context):

        # transform
        from pathlib import Path
        from src.config import DATA_DIR
        from src.transform_trips import transform_trips

        month = context["params"]["month"]
        year = context["params"]["year"]
        df = transform_trips(Path(filename), month, year)
        path = str(DATA_DIR) + f"/silver/tripdata_{month}_{year}.parquet"
        df.to_parquet(path)

        return path

    @task()
    def init_trips_task():
        from src.load_trips import init_trips

        print("init")
        init_trips()

    @task()
    def delete_existing_month_task(**context):
        month = context["params"]["month"]
        year = context["params"]["year"]
        from src.load_trips import delete_existing_month

        print("start delete")
        deleted_rows = delete_existing_month(month, year)
        return deleted_rows

    @task()
    def load(df_path):
        import pandas as pd
        from src.load_trips import load_trips

        df = pd.read_parquet(df_path)
        inserted_rows = load_trips(df)
        return inserted_rows

    filename = extract()
    df = transform(filename)
    init_trips_task() >> delete_existing_month_task() >> load(df)


nyc_trips_dag = nyc_trips_etl()
