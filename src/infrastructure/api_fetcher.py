import requests
from src.domain.mesure.raw_data import RawMeteoData


class ApiFetcher:
    """Récupère les données météo brutes depuis l'API Open Data Toulouse."""

    API_URL = (
        "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/"
        "42-station-meteo-toulouse-parc-compans-caffarelli/records"
        "?order_by=heure_utc%20desc&limit=100"
    )

    def fetch(self) -> RawMeteoData:
        """Envoie une requête à l'API et retourne les données brutes dans un RawMeteoData."""
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()  # Erreur si la requête échoue
            records = response.json().get("results", [])
            print("✅ Données brutes récupérées depuis l'API")
            return RawMeteoData(records)

        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données API : {e}")
            return RawMeteoData([])
