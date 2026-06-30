import pendulum

from airflow.sdk import dag, task
from dags_utils import on_failure_callback


@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["etl_trip"],
    # Schedule at the beggining of each mont
    schedule="0 6 1 * *",
    params={
        "month": None,
        "year": None,
        "force": False,
    },
    default_args={
        "retry_delay": pendulum.duration(minutes=5),
        "retries": 2,
        "execution_timeout": pendulum.duration(hours=1),
        "on_failure_callback": on_failure_callback,
    },
)
def nyc_trips_etl():

    @task()
    def extract(**context):
        from src.extract_trips import fetch_taxi_trip_file

        ## Take params first else context logical date
        month = context["params"]["month"] or str(context["logical_date"].month).zfill(
            2
        )
        year = context["params"]["year"] or str(context["logical_date"].year)
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

        ## Take params first else context logical date
        month = context["params"]["month"] or str(context["logical_date"].month).zfill(
            2
        )
        year = context["params"]["year"] or str(context["logical_date"].year)
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
        ## Take params first else context logical date
        month = context["params"]["month"] or str(context["logical_date"].month).zfill(
            2
        )
        year = context["params"]["year"] or str(context["logical_date"].year)
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
