from src.application.meteo_service import MeteoService

if __name__ == "__main__":
    service = MeteoService()
    service.load_data()

    print("Stations trouvées :", service.get_station_names())

    for station in service.get_data_for_station("Compans-Caffarelli"):
        print(station.temperature, station.humidite, station.pression, station.timestamp)
