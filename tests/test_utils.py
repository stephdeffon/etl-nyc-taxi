from src.utils import get_stats_on_file
import pandas as pd
import pytest

from io import StringIO, BytesIO


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {
            "trip_id": [1, 2, 3],
            "pickup_datetime": pd.to_datetime(
                ["2025-01-01 08:00", "2025-01-01 09:00", "2025-01-01 10:00"]
            ),
            "dropoff_datetime": pd.to_datetime(
                ["2025-01-01 08:30", "2025-01-01 09:45", "2025-01-01 10:20"]
            ),
            "passenger_count": [2, 1, 3],
        }
    )


@pytest.fixture
def mock_csv_file(mock_df):
    buffer = StringIO()
    mock_df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer


@pytest.fixture
def mock_parquet_file(mock_df):
    buffer = BytesIO()
    mock_df.to_parquet(buffer, index=False)
    buffer.seek(0)
    return buffer


@pytest.fixture
def mock_summary(mock_df):
    summary = {"nb_rows": len(mock_df), "nb_columns": len(mock_df.columns)}
    return summary


def test_should_get_stats_on_file_csv(mock_csv_file, mock_summary):
    assert get_stats_on_file(mock_csv_file, "csv") == mock_summary


def test_should_get_stats_on_file_parquet(mock_parquet_file, mock_summary):
    assert get_stats_on_file(mock_parquet_file) == mock_summary
