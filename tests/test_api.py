from src.infrastructure.api_fetcher import ApiFetcher

if __name__ == "__main__":
    fetcher = ApiFetcher()
    raw_data = fetcher.fetch()

    print(f"Nombre d'entrées reçues : {len(raw_data.data)}")
    if len(raw_data.data) > 0:
        print("Exemple brut : ", raw_data.data[0])
