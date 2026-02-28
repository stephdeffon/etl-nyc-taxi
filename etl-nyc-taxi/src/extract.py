from os import name

import pandas as pd
import requests
import logging
import pyarrow as pa
import argparse

from pathlib import Path



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),                 # console
        logging.FileHandler("info.log", encoding="utf-8")  # fichier
    ]
)



def get_stats_on_file(filename):
    # Read parquet file
    df = pd.read_parquet(filename,engine='pyarrow')
    summary = {
    "nb_rows": len(df),
    "nb_columns": len(df.columns),
    }
    return summary



def fetch_taxi_file(month,year,force=False):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_{year}-{month}.parquet"
    filename = Path(f"data/bronze/{year}/{month}/yellow_tripdata_{year}_{month}.parquet")
    filename.parent.mkdir(parents=True, exist_ok=True) 

    if(not filename.is_file() or force):
        with open(filename, "wb") as f:
            try:
                r = requests.get(url)
                with open(filename, 'wb') as f:
                    f.write(r.content)
                    logging.info(f"Fetched taxi file {filename}")
                    logging.info(get_stats_on_file(filename))
            except Exception as e:
                logging.error(f'Error fetching {filename}: {e}')
    else:
        logging.info(f"File {filename} already exists")
    
    


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-m','--month', dest = 'month', help = 'month in format mm', required=True)
        parser.add_argument('-y','--year', dest = 'year', help = 'year in format aaaa',required=True)
        parser.add_argument('-f','--force', dest = 'force', action='store_true', help = 'force downloadig the file even if it is alreday existing')
    except argparse.ArgumentError: 
        logging.error('Catching an argument error')
        
    args = parser.parse_args()

    (month,year,force) = (args.month,args.year,args.force)
    fetch_taxi_file(month,year,force)