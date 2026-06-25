import pandas as pd


def get_stats_on_file(filename, type="parquet"):
    """Return basic parquet or csv file statistics."""
    if type == "csv":
        df = pd.read_csv(filename, header="infer", sep=",")
        df.head()
    else:
        # Read parquet file
        df = pd.read_parquet(filename, engine="pyarrow")
    summary = {
        "nb_rows": len(df),
        "nb_columns": len(df.columns),
    }
    return summary
