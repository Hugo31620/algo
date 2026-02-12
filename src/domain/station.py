# pylint: disable=too-few-public-methods
"""
Modèle domaine représentant un état météo agrégé d'une station.

Cette classe est un conteneur de données (DTO) utilisé par le service applicatif
et l'interface graphique. Elle est volontairement minimale (pas de logique métier)
afin de respecter SRP et faciliter la sérialisation / tests.
"""

# pylint: disable=too-few-public-methods

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True)
class Station:  # pylint: disable=too-few-public-methods
    """
    Représente la dernière lecture météo connue d'une station.

    Attributs:
        name: nom de la station
        timestamp: date/heure de mesure (datetime) ou valeur équivalente
        temperature: objet Temperature (value object) ou équivalent
        humidity: objet Humidite (value object) ou équivalent
        pressure: objet Pression (value object) ou équivalent
        rain: pluie en mm si disponible
        wind_speed: vitesse du vent si disponible
        wind_direction: direction du vent en degrés si disponible

    Note:
        Certains champs peuvent être absents selon la station et les capteurs.
    """

    name: str
    timestamp: Any
    temperature: Any
    humidity: Any
    pressure: Any
    rain: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
