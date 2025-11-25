import json
import os
from datetime import datetime, timedelta
from src.domain.mesure.raw_data import RawMeteoData

class CacheManager:
    """Gère le stockage local des données brutes pour éviter trop d'appels API."""
    
    CACHE_FILE = "cache/meteo_cache.json"
    CACHE_DURATION = timedelta(hours=1)

    def is_cache_valid(self) -> bool:
        """Vérifie si le cache existe et s'il a moins d'une heure."""
        if not os.path.exists(self.CACHE_FILE):
            return False
        
        cache_time = datetime.fromtimestamp(os.path.getmtime(self.CACHE_FILE))
        return datetime.now() - cache_time < self.CACHE_DURATION

    def load_cache(self) -> RawMeteoData:
        """Charge les données du cache."""
        with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("📦 Cache chargé ✅")
        return RawMeteoData(data)

    def save_cache(self, raw_data: RawMeteoData):
        """Enregistre les données brutes dans le cache."""
        os.makedirs("cache", exist_ok=True)
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(raw_data.data, f, indent=2)
        print(" Cache mis à jour ")
