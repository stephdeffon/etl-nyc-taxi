
import pandas as pd
import os
from sqlalchemy import create_engine,text
import logging
import config
 
def get_engine():
    host=os.getenv("PG_HOST")
    user=os.getenv("PG_USER")
    pwd=os.getenv("PG_PASSWORD")
    dbname=os.getenv("PG_DB")
    port=os.getenv("PG_PORT")
    engine=create_engine(
            f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{dbname}")
    return engine

def init_db():
    logging.info("Init db. Create table fact_trips...")
    with open(f'{SQL_DIR}/ddl.sql','r') as file:
        sql_init=file.read()
    engine=get_engine()
    with engine.connect() as connection:
        result=connection.execute(text(sql_init))
    logging.info('Init db done.')

def load_dataframe(df):


    pass

if __name__ == "__main__":
    init_db()
