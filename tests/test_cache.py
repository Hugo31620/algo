from src.infrastructure.api_fetcher import ApiFetcher
from src.infrastructure.cache_manager import CacheManager

if __name__ == "__main__":
    cache = CacheManager()

    if cache.is_cache_valid():
        raw_data = cache.load_cache()
    else:
        fetcher = ApiFetcher()
        raw_data = fetcher.fetch()
        cache.save_cache(raw_data)

    print(f"➡️ Données utilisées : {len(raw_data.data)} entrées")
