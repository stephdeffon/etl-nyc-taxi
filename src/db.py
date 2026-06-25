from sqlalchemy import create_engine
from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB


def get_engine():
    """Create and return a SQLAlchemy engine for PostgreSQL."""
    engine = create_engine(
        f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )
    return engine
