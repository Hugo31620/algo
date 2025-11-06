from datetime import datetime
from src.domain.station import Station
from src.domain.mesure.temperature import Temperature
from src.domain.mesure.humidite import Humidite
from src.domain.mesure.pression import Pression

class MeteoMapper:
    """Convertit les données brutes API en objets métier formatés."""

    def record_to_station(self, record: dict) -> Station:
        temperature = Temperature(record.get('temperature_en_degre_c', 0.0))
        humidite = Humidite(record.get('humidite', 0))
        pression = Pression(record.get('pression', 0.0))

        # On privilégie l'heure de Paris pour l'affichage local
        ts_raw = record.get('heure_de_paris') or record.get('heure_utc')
        timestamp = datetime.fromisoformat(ts_raw) if ts_raw else datetime.now()

        return Station(
            name="Compans-Caffarelli",  # conserver pour l’instant
            latitude=43.6086,
            longitude=1.4356,
            temperature=temperature,
            humidite=humidite,
            pression=pression,
            pluie=record.get("pluie", 0.0),
            pluie_intensite_max=record.get("pluie_intensite_max", 0.0),
            vent_moyen=record.get("force_moyenne_du_vecteur_vent", 0.0),
            rafale_max=record.get("force_rafale_max", 0.0),
            timestamp=timestamp
        )
