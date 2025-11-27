from src.infrastructure.api_fetcher import ApiFetcher
from src.infrastructure.station_registry import StationRegistry
from src.infrastructure.meteo_mapper import MeteoMapper
from datetime import datetime


class StationDirectoryService:
    """Gère le chargement & l’accès aux données de toutes les stations."""

    def __init__(self):
        self.mapper = MeteoMapper()
        self.stations_data = {}  # { station_name: [Station, Station, …] }

    def load_all_stations(self):
        """Charge toutes les stations de StationRegistry."""
        self.stations_data = {}

        for name, endpoint in StationRegistry.get_stations().items():
            fetcher = ApiFetcher(endpoint)
            raw = fetcher.fetch()

            mapped_records = []
            for r in raw.data:
                station_obj = self.mapper.record_to_station(r, name)
                if station_obj:
                    mapped_records.append(station_obj)

            # Trier les valeurs par date UTC DESC
            mapped_records.sort(key=lambda s: s.timestamp, reverse=True)

            self.stations_data[name] = mapped_records

    def get_station_names(self):
        """Retourne la liste des noms des stations."""
        return list(self.stations_data.keys())

    def get_latest_for_station(self, station_name: str):
        """Retourne la donnée la plus récente d'une station."""
        records = self.stations_data.get(station_name, [])

        if not records:
            return None

        return records[0]  # La plus récente (trie déjà fait)
