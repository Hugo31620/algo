"""
Tests unitaires de l'agrégateur de données météo.

Ces tests vérifient que plusieurs enregistrements météo hétérogènes
sont correctement combinés pour produire une lecture complète.
"""

from src.infrastructure.reading_aggregator import aggregate_latest_values


def test_aggregate_latest_values(sample_records):
    """
    Vérifie que l'agrégateur combine correctement les dernières
    valeurs disponibles pour chaque champ météo.
    """
    agg = aggregate_latest_values(sample_records)

    assert agg["timestamp"] is not None

    assert agg["humidity_pct"] == 70.0
    assert agg["rain_mm"] == 0.0
    assert agg["temperature_c"] == 12.3

    assert agg["pressure_hpa"] is not None
    assert abs(agg["pressure_hpa"] - 1013.25) < 1e-6

    assert agg["wind_speed"] == 5.0
    assert agg["wind_direction_deg"] == 180.0
