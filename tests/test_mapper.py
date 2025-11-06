from src.infrastructure.meteo_mapper import MeteoMapper

if __name__ == "__main__":
    sample_record = {
        "temperature_en_degre_c": 14.7,
        "humidite": 81,
        "pression": 100200,
        "heure_utc": "2025-09-10T06:00:00+00:00",
        "pluie": 0.0,
        "pluie_intensite_max": 0.0,
        "force_moyenne_du_vecteur_vent": 3.2,
        "force_rafale_max": 5.1
    }

    mapper = MeteoMapper()
    station = mapper.record_to_station(sample_record)

    print(f"Température : {station.temperature}")
    print(f"Humidité : {station.humidite}")
    print(f"Pression : {station.pression}")
