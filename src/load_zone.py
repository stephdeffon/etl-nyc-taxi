from sqlalchemy import text
from src.config import log, SQL_DIR

from db import get_engine


def init_zones():
    """Initialize table 'dim_zones' by executing the DDL script."""
    log.info("Init db. Create table dim_zones...")
    with open(f"{SQL_DIR}/ddl_zones.sql", "r") as file:
        sql_init = file.read()
    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(text(sql_init))
    log.info("Init dim_zones.")


def load_zones(df):
    """Append a dataframe into dwh.dim_zone and return inserted row count."""

    engine = get_engine()
    nb_rows_inserted = df.to_sql(
        name="dim_zones",
        schema="dwh",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )
    return nb_rows_inserted


def delete_existing_zones():
    """Delete existing zones."""
    engine = get_engine()
    query = text("""
        DELETE FROM  dwh.dim_zones
    """)

    with engine.begin() as connection:
        result = connection.execute(query)

    return result.rowcount
