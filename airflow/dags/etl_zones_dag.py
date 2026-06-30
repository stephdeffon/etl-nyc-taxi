import pendulum

from airflow.sdk import dag, task


@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["etl_trip"],
    # Scheduled at the beggining of each month
    schedule="0 6 1 * *",
    params={"force": True},
)
def nyc_zones_etl():

    @task()
    def extract(**context):
        from src.extract_zone import fetch_taxi_zone_file

        force = context["params"]["force"]
        print("start extract")
        filename = fetch_taxi_zone_file(force)
        return str(filename)

    @task()
    def transform():
        from src.config import DATA_DIR
        from src.transform_zone import transform_zone

        df = transform_zone()
        path = str(DATA_DIR) + "/silver/zones.parquet"
        df.to_parquet(path, index=False)
        return path

    @task()
    def init_zone_task():
        from src.load_zone import init_zones

        print("init")
        init_zones()

    @task()
    def delete_existing_zone_task(**context):

        from src.load_zone import delete_existing_zones

        print("start delete")
        deleted_rows = delete_existing_zones()
        return deleted_rows

    @task()
    def load_zones_task(path):

        import pandas as pd
        from src.load_zone import load_zones
        from src.config import log

        df = pd.read_parquet(path)
        inserted_rows = load_zones(df)
        log.info("Rows inserted: %s", inserted_rows)
        return inserted_rows

    # extract
    filename = extract()

    # transform
    path = transform()

    filename >> path
    # load

    init_zone_task() >> delete_existing_zone_task() >> load_zones_task(path)


nyc_zone_dag = nyc_zones_etl()
