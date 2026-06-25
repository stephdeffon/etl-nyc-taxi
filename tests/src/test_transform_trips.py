import pandas as pd
import pytest
from src.transform_trips import substract_df, get_features_df, clean_df


# ─── Fixtures ────────────────────────────────────────────────────────────────
# Une fixture = données de test réutilisables dans plusieurs tests.
# pytest les injecte automatiquement dans les fonctions qui ont le même nom en paramètre.


@pytest.fixture
def raw_df():
    """DataFrame minimal qui simule un fichier parquet NYC Taxi."""
    return pd.DataFrame(
        {
            "tpep_pickup_datetime": [
                "2024-01-15 08:00:00",
                "2024-01-15 09:00:00",
                "2024-01-15 10:00:00",
            ],
            "tpep_dropoff_datetime": [
                "2024-01-15 08:30:00",
                "2024-01-15 09:45:00",
                "2024-01-15 10:20:00",
            ],
            "passenger_count": [2, 1, 3],
            "PULocationID": [100, 200, 300],
            "DOLocationID": [101, 201, 301],
            "fare_amount": [12.5, 20.0, 8.0],
            "tip_amount": [2.0, 3.5, 1.0],
            "extra_column": ["a", "b", "c"],  # colonne à supprimer
        }
    )


@pytest.fixture
def transformed_df(raw_df):
    """DataFrame après substract + get_features — prêt pour clean_df."""
    df = substract_df(raw_df)
    return get_features_df(df)


# ─── Tests substract_df ──────────────────────────────────────────────────────


def test_substract_df_garde_les_bonnes_colonnes(raw_df):
    """Vérifie que seules les 7 colonnes attendues sont conservées."""
    result = substract_df(raw_df)
    expected_cols = {
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "PULocationID",
        "DOLocationID",
        "fare_amount",
        "tip_amount",
    }
    assert set(result.columns) == expected_cols


def test_substract_df_supprime_les_colonnes_inutiles(raw_df):
    """extra_column ne doit pas survivre au substract."""
    result = substract_df(raw_df)
    assert "extra_column" not in result.columns


def test_substract_df_convertit_les_dates(raw_df):
    """Les colonnes datetime doivent être de type datetime64, pas string."""
    result = substract_df(raw_df)
    assert pd.api.types.is_datetime64_any_dtype(result["tpep_pickup_datetime"])
    assert pd.api.types.is_datetime64_any_dtype(result["tpep_dropoff_datetime"])


# ─── Tests get_features_df ───────────────────────────────────────────────────


def test_get_features_calcule_trip_duration(transformed_df):
    """Un trajet de 30 min doit avoir trip_duration = 30."""
    assert transformed_df["trip_duration"].iloc[0] == 30


def test_get_features_cree_pickup_hour(transformed_df):
    """pickup_hour doit extraire l'heure correctement."""
    assert transformed_df["pickup_hour"].iloc[0] == 8
    assert transformed_df["pickup_hour"].iloc[1] == 9


def test_get_features_cree_toutes_les_colonnes(transformed_df):
    """Les 6 colonnes de features doivent toutes exister."""
    for col in [
        "trip_duration",
        "pickup_date",
        "pickup_time",
        "pickup_hour",
        "dropoff_date",
        "dropoff_time",
        "dropoff_hour",
    ]:
        assert col in transformed_df.columns, f"Colonne manquante : {col}"


# ─── Tests clean_df ───────────────────────────────────────────────────────────


def test_clean_df_filtre_fare_negatif(transformed_df):
    """Un trajet avec fare_amount <= 0 doit être supprimé."""
    df_avec_fare_negatif = transformed_df.copy()
    df_avec_fare_negatif.loc[0, "fare_amount"] = -5.0
    result = clean_df(df_avec_fare_negatif)
    assert len(result) == 2  # 1 ligne supprimée


def test_clean_df_filtre_trajet_trop_court(transformed_df):
    """Un trajet de 0 minute ou négatif doit être supprimé."""
    df_avec_trajet_court = transformed_df.copy()
    df_avec_trajet_court.loc[0, "trip_duration"] = 0
    result = clean_df(df_avec_trajet_court)
    assert len(result) == 2


def test_clean_df_filtre_sans_passager(transformed_df):
    """Un trajet sans passager (0 ou NaN) doit être supprimé."""
    df_sans_passager = transformed_df.copy()
    df_sans_passager.loc[0, "passenger_count"] = 0
    result = clean_df(df_sans_passager)
    assert len(result) == 2


def test_clean_df_renomme_les_colonnes(transformed_df):
    """Les colonnes doivent être renommées selon la convention snake_case."""
    result = clean_df(transformed_df)
    assert "pickup_datetime" in result.columns
    assert "dropoff_datetime" in result.columns
    assert "pu_location_id" in result.columns
    assert "do_location_id" in result.columns
    # Les anciens noms ne doivent plus exister
    assert "tpep_pickup_datetime" not in result.columns
    assert "PULocationID" not in result.columns


def test_clean_df_ne_modifie_pas_les_bons_trajets(transformed_df):
    """Avec des données valides, aucune ligne ne doit être supprimée."""
    result = clean_df(transformed_df)
    assert len(result) == 3
