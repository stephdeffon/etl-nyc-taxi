from pathlib import Path
from dotenv import load_dotenv
import os



# get base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# useful paths
SQL_DIR = BASE_DIR / "sql"
DATA_DIR = BASE_DIR / "data"

# env variables
PG_HOST = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
PG_PORT = os.getenv("PG_PORT")


