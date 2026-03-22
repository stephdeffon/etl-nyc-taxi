
import pandas as pd
from sqlalchemy import create_engine,text
from config import *
from datetime import date

from db import get_engine,init_trips
 

def load_dataframe(df):
    """Append a dataframe into dwh.fact_trips and return inserted row count."""
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
    """Delete existing rows for a given source month and year."""
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
    init_trips()
    delete_existing_month('2025','02')
