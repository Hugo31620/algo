from src.infrastructure.api_fetcher import ApiFetcher
from src.infrastructure.cache_manager import CacheManager
from src.infrastructure.meteo_mapper import MeteoMapper

class MeteoService:
    """Service central qui gère la récupération, le mapping et l'accès aux données météo."""

    def __init__(self):
        self.fetcher = ApiFetcher()
        self.cache = CacheManager()
        self.mapper = MeteoMapper()
        self.stations = []  # liste de Station

    def load_data(self, force_refresh: bool = False):
        """Charge les données depuis le cache (si valide) ou l'API. force_refresh ignore le cache."""
        if not force_refresh and self.cache.is_cache_valid():
            raw_data = self.cache.load_cache()
        else:
            raw_data = self.fetcher.fetch()
            self.cache.save_cache(raw_data)

        self.stations = [self.mapper.record_to_station(record) for record in raw_data.data]

    def refresh(self):
        """Force une mise à jour depuis l'API et met à jour le cache."""
        self.load_data(force_refresh=True)

    def get_station_names(self) -> list[str]:
        return sorted(list({station.name for station in self.stations}))

    def get_data_for_station(self, name: str) -> list:
        return [s for s in self.stations if s.name == name]
