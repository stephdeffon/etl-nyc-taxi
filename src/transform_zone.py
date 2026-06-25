import pandas as pd
from src.config import log, ZONE_FILE


def clean_df_zones(df):

    # rename columns
    df = df.rename(
        columns={"LocationID": "location_id", "Borough": "borough", "Zone": "zone"}
    )

    df = df.fillna("Unknown")
    return df


def transform_zone():
    try:
        df = pd.read_csv(ZONE_FILE, header="infer", sep=",")
    except FileNotFoundError:
        log.error(f"File {ZONE_FILE} does not exists")
        return
    df = clean_df_zones(df)
    return df
