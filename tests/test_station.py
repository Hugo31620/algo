from src.domain.station import Station
from src.domain.mesure.temperature import Temperature
from src.domain.mesure.humidite import Humidite
from src.domain.mesure.pression import Pression

def test_station_object():
    station = Station(
        name="Compans",
        latitude=43.6086,
        longitude=1.4331,
        temperature=Temperature(12.3),
        humidite=Humidite(80),
        pression=Pression(101000),
        timestamp="2025-11-03T10:00:00"
    )

    print("✅ Station créée :", station.name, station.temperature, station.humidite, station.pression)
