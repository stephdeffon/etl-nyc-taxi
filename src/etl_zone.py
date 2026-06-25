from extract_zone import fetch_taxi_zone_file
from transform_zone import transform_zone
from load_zone import init_zones, load_zones, delete_existing_zones
from config import log
import argparse


def parse_args():
    """Parse CLI arguments and return (force)."""
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-f",
            "--force",
            dest="force",
            action="store_true",
            help="force downloadig the file even if it is alreday existing",
        )
    except argparse.ArgumentError:
        log.error("Catching an argument error")
    args = parser.parse_args()
    force = args.force
    return force


def main(force):
    """Run the end-to-end ETL zone workflow"""

    # extract
    fetch_taxi_zone_file(force)

    # transform
    df = transform_zone()

    # load
    init_zones()

    deleted_rows = delete_existing_zones()
    log.info("Deleted %s existing rows", deleted_rows)

    inserted_rows = load_zones(df)
    log.info("Rows inserted: %s", inserted_rows)

    if deleted_rows != inserted_rows and deleted_rows > 0:
        log.warning(
            "Rows deleted different than rows inserted. Before: %s / After: %s",
            deleted_rows,
            inserted_rows,
        )


if __name__ == "__main__":
    log.info("ETL Zone Starting...")
    force = parse_args()
    main(force)
    log.info("ETL Zone Done...")
