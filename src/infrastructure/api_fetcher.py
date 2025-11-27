import requests
from src.domain.mesure.raw_data import RawMeteoData


class ApiFetcher:
    """Récupère les données météo brutes depuis l'API Open Data Toulouse."""

    def __init__(self, endpoint: str, limit: int = 100):
        self.url = f"{endpoint}&limit={limit}"

    def fetch(self) -> RawMeteoData:
        """Requête API → RawMeteoData."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            print(f"✅ Données récupérées depuis : {self.url}")

            records = response.json().get("results", [])
            return RawMeteoData(records)

        except Exception as e:
            print(f"❌ Erreur API ({self.url}) : {e}")
            return RawMeteoData([])
