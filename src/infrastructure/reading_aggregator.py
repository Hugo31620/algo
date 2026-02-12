"""
Agrégation des données météo brutes.

Ce module combine plusieurs enregistrements météo hétérogènes
afin de reconstruire une lecture complète en utilisant les
dernières valeurs non nulles disponibles pour chaque champ.
"""

from datetime import datetime

from src.infrastructure.record_extractor import (
    extract_timestamp,
    extract_temperature_c,
    extract_humidity_pct,
    extract_pressure_hpa,
    extract_rain_mm,
    extract_wind_speed,
    extract_wind_direction_deg,
)


def aggregate_latest_values(records: list[dict]) -> dict:
    """
    Agrège une liste d'enregistrements météo bruts.

    La fonction parcourt les enregistrements du plus récent au plus ancien
    et récupère, pour chaque champ, la première valeur non nulle rencontrée.

    Args:
        records: liste de dictionnaires représentant les données brutes

    Returns:
        Dictionnaire contenant les valeurs agrégées.
    """
    sorted_records = sorted(
        records,
        key=lambda r: extract_timestamp(r) or datetime.min,
        reverse=True,
    )

    timestamp = None
    temperature_c = None
    humidity_pct = None
    pressure_hpa = None
    rain_mm = None
    wind_speed = None
    wind_direction_deg = None

    for record in sorted_records:
        if timestamp is None:
            timestamp = extract_timestamp(record)

        if temperature_c is None:
            temperature_c = extract_temperature_c(record)

        if humidity_pct is None:
            humidity_pct = extract_humidity_pct(record)

        if pressure_hpa is None:
            pressure_hpa = extract_pressure_hpa(record)

        if rain_mm is None:
            rain_mm = extract_rain_mm(record)

        if wind_speed is None:
            wind_speed = extract_wind_speed(record)

        if wind_direction_deg is None:
            wind_direction_deg = extract_wind_direction_deg(record)

        if all(
            value is not None
            for value in (
                timestamp,
                temperature_c,
                humidity_pct,
                pressure_hpa,
                rain_mm,
                wind_speed,
                wind_direction_deg,
            )
        ):
            break

    return {
        "timestamp": timestamp,
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "pressure_hpa": pressure_hpa,
        "rain_mm": rain_mm,
        "wind_speed": wind_speed,
        "wind_direction_deg": wind_direction_deg,
    }
