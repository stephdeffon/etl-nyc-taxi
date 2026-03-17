from pathlib import Path
from dotenv import load_dotenv
import os
import logging as log

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[
        log.StreamHandler(),                 # console
        log.FileHandler("info.log", encoding="utf-8")  # fichier
    ]
)




# get base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# useful paths
SQL_DIR = BASE_DIR / "sql"
DATA_DIR = BASE_DIR / "data"

# loading .env
load_dotenv(BASE_DIR / ".env")

# env variables
PG_HOST = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
PG_PORT = os.getenv("PG_PORT")


