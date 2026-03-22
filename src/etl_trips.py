from numpy import insert

from extract_trips import fetch_taxi_trips_file
from transform_trips import transform
from load_trips import init_db, load_dataframe, delete_existing_month
from config import *
from utils import get_stats_on_file
import argparse


def parse_args():
    """Parse CLI arguments and return (month, year, force)."""
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
    return (month, year, force)


def main(month,year,force):
    """Run the end-to-end ETL workflow for a given month and year."""

    
    #extract
    filename = fetch_taxi_trips_file(month, year, force)

    #transform
    df = transform(filename,month,year)

    #load
    init_db()
    deleted_rows = delete_existing_month(month, year)
    log.info("Deleted %s existing rows for %s-%s", deleted_rows, month, year)
    
    inserted_rows = load_dataframe(df)
    log.info('Rows inserted: %s',inserted_rows)

    if(deleted_rows != inserted_rows and deleted_rows > 0):
        log.warning('Rows deleted different than rows inserted for %s-%s. Before: %s / After: %s', month, year, deleted_rows, inserted_rows) 

    log.info('ETL Done...')

   

if __name__ == "__main__":
    log.info('ETL Starting...')
    (month, year, force) = parse_args()
    main(month, year, force)
