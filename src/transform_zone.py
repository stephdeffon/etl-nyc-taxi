from fileinput import filename

import pandas as pd
from config import *
import argparse

filename = ZONE_FILE


def clean_df_zones(df): 


     # rename columns
    df = df.rename(columns={
    "LocationID": "location_id",
    "Borough" :"borough",
    "Zone": "zone"
    })  
    return df
    


def transform_zone():
    try:
        df = pd.read_csv(filename,header='infer',sep=',')
    except FileNotFoundError:
        log.error(f'File {filename} does not exists')
        return 
    df = clean_df_zones(df)
    return df

