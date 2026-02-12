"""
Tests unitaires du module record_extractor.

Ces tests vérifient l'extraction correcte des différents champs
depuis des enregistrements météo bruts.
"""

from src.infrastructure.record_extractor import (
    extract_timestamp,
    extract_temperature_c,
    extract_humidity_pct,
    extract_pressure_hpa,
    extract_rain_mm,
    extract_wind_speed,
    extract_wind_direction_deg,
)


def test_extract_timestamp_iso():
    """
    Vérifie l'extraction d'un timestamp au format ISO.
    """
    record = {"heure_utc": "2026-01-20T10:00:00Z"}
    ts = extract_timestamp(record)
    assert ts is not None
    assert ts.isoformat().startswith("2026-01-20T10:00:00")


def test_extract_temperature_key_variants():
    """
    Vérifie l'extraction de la température.
    """
    record = {"temperature_en_degre_c": 12.3}
    assert extract_temperature_c(record) == 12.3


def test_extract_humidity_key_variants():
    """
    Vérifie l'extraction de l'humidité relative.
    """
    record = {"humidite": 70}
    assert extract_humidity_pct(record) == 70.0


def test_extract_pressure_pa_to_hpa():
    """
    Vérifie la conversion de la pression de Pa vers hPa.
    """
    record = {"pression": 101325}
    pressure = extract_pressure_hpa(record)
    assert pressure is not None
    assert abs(pressure - 1013.25) < 1e-6


def test_extract_wind_speed_and_direction():
    """
    Vérifie l'extraction de la vitesse et de la direction du vent.
    """
    record = {
        "force_moyenne_du_vecteur_vent": 5.0,
        "direction_du_vecteur_vent_moyen": 180,
    }
    assert extract_wind_speed(record) == 5.0
    assert extract_wind_direction_deg(record) == 180.0


def test_extract_rain():
    """
    Vérifie l'extraction de la pluie.
    """
    record = {"pluie": 0.0}
    assert extract_rain_mm(record) == 0.0


def test_extract_supports_nested_data_object():
    """
    Vérifie la prise en charge d'un enregistrement imbriqué (clé 'data').
    """
    record = {
        "data": {
            "temperature_en_degre_c": 9.5,
            "heure_utc": "2026-01-20T10:00:00Z",
        }
    }
    assert extract_temperature_c(record) == 9.5
    assert extract_timestamp(record) is not None
