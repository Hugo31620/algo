from datetime import datetime
from src.domain.mesure.temperature import Temperature
from src.domain.mesure.humidite import Humidite
from src.domain.mesure.pression import Pression

class Station:
    """Représente une station météo structurée avec mesures nettoyées."""

    def __init__(self, name: str, latitude: float, longitude: float,
                 temperature: Temperature, humidite: Humidite,
                 pression: Pression, 
                 pluie: float, pluie_intensite_max: float,
                 vent_moyen: float, rafale_max: float,
                 timestamp: datetime):
        
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidite = humidite
        self.pression = pression
        self.pluie = pluie
        self.pluie_intensite_max = pluie_intensite_max
        self.vent_moyen = vent_moyen
        self.rafale_max = rafale_max
        self.timestamp = timestamp
