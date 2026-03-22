from sqlalchemy import create_engine,text
from config import *
  

def get_engine():
    """Create and return a SQLAlchemy engine for PostgreSQL."""
    engine=create_engine(
            f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
    return engine

def init_trips():
    """Initialize table 'fact_trips' by executing the DDL script."""
    log.info("Init db. Create table fact_trips...")
    with open(f'{SQL_DIR}/ddl_trips.sql','r') as file:
        sql_init=file.read()
    engine=get_engine()
    with engine.begin() as connection:
        result=connection.execute(text(sql_init))
    log.info('Init fact_trips done.')


def init_zones():
    """Initialize table 'dim_zones' by executing the DDL script."""
    log.info("Init db. Create table dim_zones...")
    with open(f'{SQL_DIR}/ddl_zones.sql','r') as file:
        sql_init=file.read()
    engine=get_engine()
    with engine.begin() as connection:
        result=connection.execute(text(sql_init))
    log.info('Init dim_zones.')

