
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
    with engine.connect() as connection:
        result=connection.execute(text(sql_init))
    log.info('Init db done.')

def load_dataframe(df):


    pass

if __name__ == "__main__":
    init_db()
