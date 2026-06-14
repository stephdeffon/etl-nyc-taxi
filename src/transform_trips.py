import pandas as pd
from src.config import *
import argparse

def substract_df(df):
    """Select required columns and cast date fields to datetime."""

    cols_to_keep = ['tpep_pickup_datetime','tpep_dropoff_datetime',
                'passenger_count','PULocationID','DOLocationID',
                'fare_amount','tip_amount']
    df_substracted= df[cols_to_keep]

    ## clean date time
    dt_cols = ['tpep_pickup_datetime','tpep_dropoff_datetime']

    for col in dt_cols:
        df_substracted[col] = pd.to_datetime(df_substracted[col],errors='coerce')

    return df_substracted


def get_features_df(df):
    """Create time-based features and trip duration in minutes."""
    df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds().div(60).astype(int)
    df['pickup_date'] = df['tpep_pickup_datetime'].dt.date
    df['pickup_time'] = df['tpep_pickup_datetime'].dt.time
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    df['dropoff_date'] = df['tpep_dropoff_datetime'].dt.date
    df['dropoff_time'] = df['tpep_dropoff_datetime'].dt.time
    df['dropoff_hour'] = df['tpep_dropoff_datetime'].dt.hour
    return df

def clean_df(df):
    """Filter invalid trips and rename columns for downstream consumption."""
    
    initial_rows_count = len(df)

    # Remove trips with fare negative or null
    df_clean = df.loc[df['fare_amount']>0]

    # Remove trips with duration less than a minute or negative
    df_clean = df_clean.loc[df_clean["trip_duration"]>0]

    # Remove trips with drop off datetime earlier than pick up time
    df_clean = df_clean.loc[df_clean['tpep_pickup_datetime'] < df_clean['tpep_dropoff_datetime']]

    # Remove trips without passengers
    df_clean = df_clean.fillna({'passenger_count':0})
    df_clean = df_clean.loc[df_clean['passenger_count'] > 0]

    final_rows_count = len(df_clean)

    # rename columns
    df_clean = df_clean.rename(columns={
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
    "PULocationID": "pu_location_id",
    "DOLocationID": "do_location_id",
})

    log.info(f"Rows before: {initial_rows_count}")
    log.info(f"Rows after: {final_rows_count}")
    log.info(f"Rows removed: {initial_rows_count - final_rows_count}")

    return df_clean   

def transform_trips(filename,month,year):
    """Run the full transform pipeline and attach source partition metadata."""
    try:
        df = pd.read_parquet(filename,engine='pyarrow')
    except FileNotFoundError:
        log.error(f'File {filename} does not exists')
        return 
    df = substract_df(df)
    df = get_features_df(df)
    df = clean_df(df)
    df['source_month'] = int(month)
    df['source_year'] = int(year)
    return df



if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f','--filename', dest = 'filename', help = 'filename in parquet format', required=True)
    except argparse.ArgumentError: 
        log.error('Catching an argument error')
        
    args = parser.parse_args()

    transform_trips(args.filename)
