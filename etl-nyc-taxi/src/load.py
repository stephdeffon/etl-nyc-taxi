
import pandas as pd
from sqlalchemy import create_engine,text
from config import *
 
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
    df.to_sql(
        name="fact_trips",
        schema="dwh",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=100000,
        method='multi'
    )

from datetime import date
from sqlalchemy import text

def delete_existing_month(year, month):
    engine = get_engine()

    year = int(year)
    month = int(month)

    month_start = date(year, month, 1)

    if month == 12:
        next_month_start = date(year + 1, 1, 1)
    else:
        next_month_start = date(year, month + 1, 1)

    query = text("""
        DELETE FROM dwh.fact_trips
        WHERE pickup_date >= :month_start
          AND pickup_date < :next_month_start
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "month_start": month_start,
                "next_month_start": next_month_start,
            }
        )

    return result.rowcount


if __name__ == "__main__":
    init_db()
