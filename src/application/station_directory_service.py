"""
Service applicatif d'accès aux données météo.

Ce module contient le service principal utilisé par l'interface graphique.
Il orchestre :
- la liste des stations disponibles (via un catalogue)
- la récupération des données (via une stratégie MeteoClient)
- un cache en mémoire (dictionnaire) avec TTL
"""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Optional, Protocol

from src.infrastructure.station_registry import StationRegistry
from src.infrastructure.reading_aggregator import aggregate_latest_values
from src.domain.station import Station
from src.domain.mesure.temperature import Temperature
from src.domain.mesure.humidite import Humidite
from src.domain.mesure.pression import Pression
from src.infrastructure.meteo_clients import MeteoClient, HttpMeteoClient


class StationCatalog(Protocol):  # pylint: disable=too-few-public-methods
    """
    Port (interface) permettant d'obtenir les stations disponibles.

    Ce port facilite l'injection de dépendances (DIP) et la testabilité.
    """

    def get_stations(self) -> dict[str, str]:
        """
        Retourne un dictionnaire station -> endpoint.
        """
        raise NotImplementedError


@dataclass
class DefaultStationCatalog:
    """
    Implémentation par défaut du catalogue de stations.

    Cette classe est volontairement minimale (1 méthode publique) :
    son rôle est uniquement d'adapter StationRegistry au port StationCatalog.
    """

    def get_stations(self) -> dict[str, str]:
        """
        Retourne la liste des stations depuis le registry.
        """
        return StationRegistry.get_stations()


class StationDirectoryService:
    """
    Service applicatif principal.

    Responsabilités :
    - fournir la liste des stations
    - récupérer la dernière lecture pour une station
    - mettre en cache en mémoire (dictionnaire) les résultats récents
    """

    def __init__(
        self,
        catalog: StationCatalog | None = None,
        client: MeteoClient | None = None,
        cache_ttl_seconds: int = 60,
    ):
        """
        Initialise le service.

        Args:
            catalog: source des stations (station -> endpoint)
            client: stratégie de récupération des données (HTTP, mock, etc.)
            cache_ttl_seconds: durée de validité du cache mémoire
        """
        self._catalog = catalog or DefaultStationCatalog()
        self._client: MeteoClient = client or HttpMeteoClient(timeout_seconds=10)
        self._cache_ttl_seconds = cache_ttl_seconds

        # Dictionnaire (barème): cache en mémoire
        # cache[station_name] = {"expires_at": float, "value": Station}
        self._cache: dict[str, dict] = {}

    def get_station_names(self) -> list[str]:
        """
        Retourne la liste des noms de stations disponibles.
        """
        return list(self._catalog.get_stations().keys())

    def _cache_get(self, station_name: str) -> Optional[Station]:
        """
        Récupère une valeur du cache si elle est présente et non expirée.

        Args:
            station_name: nom de la station

        Returns:
            Station si disponible en cache, sinon None.
        """
        item = self._cache.get(station_name)
        if not item:
            return None

        expires_at = item.get("expires_at")
        value = item.get("value")

        if not isinstance(expires_at, (int, float)) or time() > expires_at:
            self._cache.pop(station_name, None)
            return None

        return value if isinstance(value, Station) else None

    def _cache_set(self, station_name: str, value: Station) -> None:
        """
        Stocke une valeur dans le cache avec expiration.

        Args:
            station_name: nom de la station
            value: objet Station à mettre en cache
        """
        self._cache[station_name] = {
            "expires_at": time() + self._cache_ttl_seconds,
            "value": value,
        }

    def get_latest_for_station(self, station_name: str) -> Optional[Station]:
        """
        Retourne la dernière lecture météo disponible pour une station.

        Stratégie :
        - check cache (dictionnaire)
        - appel API (via MeteoClient)
        - agrégation des champs (records hétérogènes)
        - construction d'une Station (domain)

        Args:
            station_name: nom de la station

        Returns:
            Station si des données exploitables existent, sinon None.
        """
        cached = self._cache_get(station_name)
        if cached is not None:
            return cached

        stations = self._catalog.get_stations()
        endpoint = stations.get(station_name)
        if not endpoint:
            return None

        raw_data = self._client.fetch(endpoint)
        if raw_data is None or not getattr(raw_data, "data", None):
            return None

        agg = aggregate_latest_values(raw_data.data)
        if agg.get("timestamp") is None:
            return None

        station = Station(
            name=station_name,
            timestamp=agg["timestamp"],
            temperature=Temperature(agg.get("temperature_c")),
            humidity=Humidite(agg.get("humidity_pct")),
            pressure=Pression(agg.get("pressure_hpa")),
            rain=agg.get("rain_mm"),
            wind_speed=agg.get("wind_speed"),
            wind_direction=agg.get("wind_direction_deg"),
        )

        self._cache_set(station_name, station)
        return station
