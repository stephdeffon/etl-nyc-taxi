from os import name
import requests
import argparse
from src.utils import get_stats_on_file
from src.config import *
from pathlib import Path







def fetch_taxi_zone_file(force=False):
    """Download a monthly taxi parquet file into the bronze layer."""
    url = f"https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    filename = ZONE_FILE
    filename.parent.mkdir(parents=True, exist_ok=True) 
    if(not filename.is_file() or force):
        with open(filename, "wb") as f:
            try:
                r=requests.get(url)
                with open(filename, 'wb') as f:
                    f.write(r.content)
                    log.info(f"Fetched taxi zone file {filename}")
                    
            except Exception as e:
                log.error(f'Error fetching {filename}: {e}')
        log.info(get_stats_on_file(filename,'csv'))
    else:
        log.info(f"File {filename} already exists")
    return filename
    

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--force',
                            dest='force',
                            action='store_true', help='force downloadig the file even if it is alreday existing')
    except argparse.ArgumentError:
        log.error('Catching an argument error')   
    args = parser.parse_args()
    force = args.force
    fetch_taxi_zone_file(force)
