class StationRegistry:
    """Liste des stations météo + URLs API complètes."""

    BASE = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/"

    STATIONS = {
        "Compans-Caffarelli":
            BASE +
            "42-station-meteo-toulouse-parc-compans-cafarelli/records?order_by=heure_utc%20desc",

        "Université Paul Sabatier":
            BASE +
            "37-station-meteo-toulouse-universite-paul-sabatier/records?order_by=heure_utc%20desc",

        "Pech David":
            BASE +
            "13-station-meteo-toulouse-pech-david/records?order_by=heure_utc%20desc",
    }

    @classmethod
    def get_stations(cls):
        return cls.STATIONS
