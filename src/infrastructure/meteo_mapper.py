from datetime import datetime
from src.domain.station import Station
from src.domain.mesure.temperature import Temperature
from src.domain.mesure.humidite import Humidite
from src.domain.mesure.pression import Pression


class MeteoMapper:
    """Convertit les données brutes API en objets Station."""

    def _safe_float(self, value, default=0.0):
        """Convertit proprement une valeur en float."""
        try:
            if value is None or value == "":
                return default
            return float(value)
        except Exception:
            return default

    def _parse_timestamp(self, record):
        """Retourne un timestamp propre et fiable."""

        raw = record.get("heure_de_paris") or record.get("heure_utc")
        if not raw:
            return None

        try:
            ts = datetime.fromisoformat(raw)

            # Filtre de sécurité : pas de dates absurdes
            if 2020 <= ts.year <= datetime.now().year + 1:
                return ts
            return None

        except Exception:
            return None

    def record_to_station(self, record: dict, station_name: str):
        """Transforme un enregistrement API en objet Station."""

        timestamp = self._parse_timestamp(record)
        if timestamp is None:
            return None  # ligne ignorée car date invalide

        temperature = Temperature(self._safe_float(record.get("temperature_en_degre_c")))
        humidite = Humidite(self._safe_float(record.get("humidite")))
        pression = Pression(self._safe_float(record.get("pression"), 100000))

        pluie = self._safe_float(record.get("pluie"))
        pluie_intensite_max = self._safe_float(record.get("pluie_intensite_max"))
        vent_moyen = self._safe_float(record.get("force_moyenne_du_vecteur_vent"))
        rafale_max = self._safe_float(record.get("force_rafale_max"))

        return Station(
            name=station_name,
            latitude=0.0,
            longitude=0.0,
            temperature=temperature,
            humidite=humidite,
            pression=pression,
            pluie=pluie,
            pluie_intensite_max=pluie_intensite_max,
            vent_moyen=vent_moyen,
            rafale_max=rafale_max,
            timestamp=timestamp,
        )
