from sqlalchemy import create_engine,text
from config import *
  

def get_engine():
    """Create and return a SQLAlchemy engine for PostgreSQL."""
    engine=create_engine(
            f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
    return engine




