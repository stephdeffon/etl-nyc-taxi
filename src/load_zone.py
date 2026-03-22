import pandas as pd
from sqlalchemy import text
from config import *
from datetime import date

from db import get_engine,init_zones


def load_zones(df):
    """Append a dataframe into dwh.dim_zone and return inserted row count."""

    # init table fact_trips
    init_zones()
    
    engine = get_engine()
    nb_rows_inserted = df.to_sql(
        name="dim_zones",
        schema="dwh",
        con=engine,
        if_exists="append",
        index=False,
        method='multi'
    )
    return nb_rows_inserted



def delete_existing_zones():
    """Delete existing zones."""
    engine = get_engine()
    query = text("""
        TRUNCATE  dwh.dim_zones
    """)

    with engine.begin() as connection:
        result = connection.execute(        )

    return result.rowcount