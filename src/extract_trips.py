from os import name

import pandas as pd
import requests
import pyarrow as pa
import argparse
from src.config import *
from src.utils import get_stats_on_file

from pathlib import Path




def fetch_taxi_trip_file(month, year, force=False):
    """Download a monthly taxi parquet file into the bronze layer."""
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month}.parquet"
    filename = Path(f"{DATA_DIR}/bronze/yellow_tripdata_{year}_{month}.parquet")
    filename.parent.mkdir(parents=True, exist_ok=True) 
    if(not filename.is_file() or force):
        with open(filename, "wb") as f:
            try:
                r=requests.get(url)
                with open(filename, 'wb') as f:
                    f.write(r.content)
                    log.info(f"Fetched taxi file {filename}")
                    log.info(get_stats_on_file(filename))
            except Exception as e:
                log.error(f'Error fetching {filename}: {e}')
    else:
        log.info(f"File {filename} already exists")
    return filename
    

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--month',
                            dest='month', help='month in format mm', required=True)
        parser.add_argument('-y', '--year',
                            dest='year', help='year in format aaaa', required=True)
        parser.add_argument('-f', '--force',
                            dest='force',
                            action='store_true', help='force downloadig the file even if it is alreday existing')
    except argparse.ArgumentError:
        log.error('Catching an argument error')   
    args = parser.parse_args()
    (month, year, force) = (args.month, args.year, args.force)
    fetch_taxi_trip_file(month, year, force)
