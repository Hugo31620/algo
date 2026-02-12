"""
Extraction de champs depuis des enregistrements météo bruts.

Ce module centralise la lecture des champs dans les dictionnaires reçus
depuis l'API (keys variables selon les stations/datasets). Il fournit des
fonctions d'extraction robustes et réutilisables pour l'agrégation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional


def first_value(record: dict, *keys: str) -> Any:
    """
    Retourne la première valeur non nulle trouvée pour une liste de clés.

    Supporte un schéma imbriqué lorsque l'enregistrement contient une clé
    'data' de type dictionnaire.

    Args:
        record: dictionnaire brut (potentiellement avec record["data"])
        *keys: clés candidates à tester

    Returns:
        La première valeur non nulle trouvée, sinon None.
    """
    inner = record.get("data") if isinstance(record.get("data"), dict) else record

    for key in keys:
        if key in inner and inner[key] is not None:
            return inner[key]
        if key in record and record[key] is not None:
            return record[key]
    return None


def parse_datetime(value: Any) -> Optional[datetime]:
    """
    Convertit une valeur ISO 8601 en datetime.

    Args:
        value: valeur texte/objet convertible en chaîne

    Returns:
        datetime si parsing OK, sinon None.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def to_float(value: Any) -> Optional[float]:
    """
    Convertit une valeur en float.

    Args:
        value: valeur convertible (str, int, float)

    Returns:
        float si conversion OK, sinon None.
    """
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_timestamp(record: dict) -> Optional[datetime]:
    """
    Extrait le timestamp de l'enregistrement.

    Args:
        record: dictionnaire brut

    Returns:
        datetime si disponible, sinon None.
    """
    return parse_datetime(
        first_value(
            record,
            "heure_de_paris",
            "heure_utc",
            "date",
            "datetime",
            "timestamp",
            "time",
        )
    )


def extract_temperature_c(record: dict) -> Optional[float]:
    """
    Extrait la température en degrés Celsius.

    Args:
        record: dictionnaire brut

    Returns:
        Température en °C si disponible, sinon None.
    """
    return to_float(
        first_value(
            record,
            "temperature_en_degre_c",
            "temperature_air",
            "temp_air",
            "temperature",
            "temp",
            "temp_c",
            "temperature_c",
            "ta",
            "t",
        )
    )


def extract_humidity_pct(record: dict) -> Optional[float]:
    """
    Extrait l'humidité relative en pourcentage.

    Args:
        record: dictionnaire brut

    Returns:
        Humidité en % si disponible, sinon None.
    """
    return to_float(
        first_value(
            record,
            "humidite",
            "humidite_relative",
            "humidite_relative_en_pourcentage",
            "hygrometrie",
            "hr",
            "u",
        )
    )


def extract_pressure_hpa(record: dict) -> Optional[float]:
    """
    Extrait la pression atmosphérique.

    Conversion automatique Pa -> hPa si nécessaire.

    Args:
        record: dictionnaire brut

    Returns:
        Pression en hPa si disponible, sinon None.
    """
    pressure = to_float(
        first_value(
            record,
            "pression",
            "pression_atmo",
            "pression_atmospherique",
            "pressure",
            "pres",
            "ps",
            "p",
            "qnh",
        )
    )
    if pressure is None:
        return None

    if pressure > 2000:
        return pressure / 100.0

    return pressure


def extract_rain_mm(record: dict) -> Optional[float]:
    """
    Extrait la pluie en mm.

    Args:
        record: dictionnaire brut

    Returns:
        Pluie en mm si disponible, sinon None.
    """
    return to_float(
        first_value(
            record,
            "pluie",
            "precipitations",
            "rain",
            "rr",
        )
    )


def extract_wind_speed(record: dict) -> Optional[float]:
    """
    Extrait une mesure de vitesse de vent (moyenne ou rafale).

    Args:
        record: dictionnaire brut

    Returns:
        Vitesse de vent si disponible, sinon None.
    """
    wind_speed = to_float(
        first_value(
            record,
            "force_moyenne_du_vecteur_vent",
            "vent_vitesse",
            "vitesse_vent",
            "wind_speed",
            "ff",
        )
    )
    if wind_speed is not None:
        return wind_speed

    return to_float(first_value(record, "force_rafale_max"))


def extract_wind_direction_deg(record: dict) -> Optional[float]:
    """
    Extrait la direction du vent en degrés.

    Args:
        record: dictionnaire brut

    Returns:
        Direction en degrés si disponible, sinon None.
    """
    return to_float(
        first_value(
            record,
            "direction_du_vecteur_vent_moyen",
            "direction_du_vecteur_de_vent_max_en_degres",
            "vent_direction",
            "direction_vent",
            "wind_dir",
            "dd",
        )
    )
