import pandas as pd
import pytest

from src.transform_zone import clean_df_zones


@pytest.fixture
def raw_df():
    """DataFrame minimal qui simule un fichier zone NYC Taxi."""
    return pd.DataFrame(
        {
            "LocationID": ["1", "2", "3"],
            "Borough": ["2A", "3A", "A4"],
            "Zone": [2, 1, 3],
        }
    )


def test_clean_df_should_have_renamed_columns(raw_df):
    expected_cols = {"location_id", "borough", "zone"}

    result = clean_df_zones(raw_df)

    assert set(result.columns) == expected_cols
