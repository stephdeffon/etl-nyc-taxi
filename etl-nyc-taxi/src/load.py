
import pandas as pd
from sqlalchemy import create_engine,text
from config import *
from datetime import date
 
def get_engine():
    engine=create_engine(
            f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
    return engine

def init_db():
    log.info("Init db. Create table fact_trips...")
    with open(f'{SQL_DIR}/ddl.sql','r') as file:
        sql_init=file.read()
    engine=get_engine()
    with engine.begin() as connection:
        result=connection.execute(text(sql_init))
    log.info('Init db done.')

def load_dataframe(df):
    engine = get_engine()
    nb_rows_inserted = df.to_sql(
        name="fact_trips",
        schema="dwh",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=100000,
        method='multi'
    )
    return nb_rows_inserted



def delete_existing_month(month, year):
    engine = get_engine()

    year = int(year)
    month = int(month)

    query = text("""
        DELETE FROM dwh.fact_trips
        WHERE source_month = :month
          AND source_year = :year
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "month": month,
                "year": year,
            }
        )

    return result.rowcount


if __name__ == "__main__":
    init_db()
    delete_existing_month('2025','02')
