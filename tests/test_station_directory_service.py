"""
Tests unitaires du service StationDirectoryService.

Ces tests vérifient :
- la récupération des stations
- l'utilisation du cache (dictionnaire)
- le comportement en cas de station inconnue
"""

from dataclasses import dataclass

from src.application.station_directory_service import StationDirectoryService
from src.domain.station import Station


@dataclass
class FakeRawData:
    """
    Faux conteneur de données brutes.

    Simule l'objet RawMeteoData retourné par un client météo.
    """

    data: list[dict]


class FakeCatalog:  # pylint: disable=too-few-public-methods
    """
    Faux catalogue de stations.

    Utilisé pour injecter une liste contrôlée de stations dans les tests.
    """

    def __init__(self, stations: dict[str, str]):
        """
        Initialise le catalogue fake.

        Args:
            stations: dictionnaire station -> endpoint
        """
        self._stations = stations

    def get_stations(self) -> dict[str, str]:
        """
        Retourne les stations configurées pour le test.
        """
        return self._stations


class FakeClient:  # pylint: disable=too-few-public-methods
    """
    Faux client météo.

    Compte le nombre d'appels afin de vérifier le fonctionnement du cache.
    """

    def __init__(self, raw_data: FakeRawData):
        """
        Initialise le client fake.

        Args:
            raw_data: données brutes à retourner lors de fetch()
        """
        self._raw_data = raw_data
        self.calls = 0

    def fetch(self, _endpoint: str):
        """
        Simule un appel API.

        Args:
            _endpoint: endpoint non utilisé (signature conforme)

        Returns:
            FakeRawData fourni au constructeur.
        """
        self.calls += 1
        return self._raw_data


def test_service_returns_station_and_uses_cache(sample_records):
    """
    Vérifie que le service retourne une Station et utilise le cache.
    """
    catalog = FakeCatalog({"Compans-Caffarelli": "endpoint://x"})
    client = FakeClient(FakeRawData(sample_records))

    service = StationDirectoryService(
        catalog=catalog,
        client=client,
        cache_ttl_seconds=9999,
    )

    station_1 = service.get_latest_for_station("Compans-Caffarelli")
    assert isinstance(station_1, Station)
    assert client.calls == 1

    station_2 = service.get_latest_for_station("Compans-Caffarelli")
    assert isinstance(station_2, Station)
    assert client.calls == 1  # cache utilisé

    assert station_1.name == "Compans-Caffarelli"
    assert station_1.timestamp is not None
    assert hasattr(station_1.temperature, "value")
    assert hasattr(station_1.humidity, "value")
    assert hasattr(station_1.pressure, "value")


def test_service_unknown_station_returns_none(sample_records):
    """
    Vérifie qu'une station inconnue retourne None sans appel client.
    """
    catalog = FakeCatalog({"A": "endpoint://a"})
    client = FakeClient(FakeRawData(sample_records))

    service = StationDirectoryService(
        catalog=catalog,
        client=client,
        cache_ttl_seconds=0,
    )

    result = service.get_latest_for_station("UNKNOWN")
    assert result is None
    assert client.calls == 0
