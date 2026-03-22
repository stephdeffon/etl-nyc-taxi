from fileinput import filename

import pandas as pd
from config import *
import argparse

filename = ZONE_FILE

def transform_zone():
    try:
        df = pd.read_csv(filename,header='infer',sep=',')
    except FileNotFoundError:
        log.error(f'File {filename} does not exists')
        return 
    
    return df