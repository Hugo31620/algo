from typing import List

class ConsoleView:
    """Vue console simple pour afficher les données météo."""

    def __init__(self, service):
        self.service = service

    def run(self):
        """Affiche la liste des stations, sélection puis dernière mesure valide (rafraîchie)."""
        #  On force un rafraîchissement pour ne pas lire un vieux cache
        self.service.load_data(force_refresh=True)

        stations = self.service.get_station_names()

        print("\nStations météo disponibles :")
        for index, name in enumerate(stations, start=1):
            print(f"{index}. {name}")

        try:
            choice = int(input("\nChoisissez une station par numéro : ")) - 1
        except ValueError:
            print("Veuillez entrer un nombre valide. Fin du programme.")
            return

        if not (0 <= choice < len(stations)):
            print("Choix invalide, fin du programme.")
            return

        selected_station = stations[choice]
        print(f"\nDonnées pour la station : {selected_station}\n")

        records = self.service.get_data_for_station(selected_station)
        if not records:
            print("Aucune donnée disponible.")
            return

        valid_records = self._filter_valid_records(records)
        if not valid_records:
            print("Aucune donnée valide trouvée (valeurs aberrantes filtrées).")
            return

        latest = max(valid_records, key=lambda r: r.timestamp)
        self._display_record(latest)

    # -------- Méthodes internes --------

    def _filter_valid_records(self, records) -> List:
        """Supprime les données météos aberrantes (capteur en erreur)."""
        def parse_float(value: str):
            return float(value.replace("°C", "").replace("%", "").replace("Pa", "").replace(",", ".").strip())

        valid = []
        for r in records:
            try:
                temp = parse_float(str(r.temperature.value))
                hum = parse_float(str(r.humidite.value))
                pres = parse_float(str(r.pression.value))

                if not (-30 <= temp <= 50):   # fenêtre raisonnable Toulouse
                    continue
                if not (1 <= hum <= 100):
                    continue
                if not (95000 <= pres <= 105000):
                    continue

                valid.append(r)
            except Exception:
                continue
        return valid

    def _display_record(self, record):
        print(f"Date/Heure : {record.timestamp}")
        print(f" - Température : {record.temperature}")
        print(f" - Humidité : {record.humidite}")
        print(f" - Pression : {record.pression}")
        print(f" - Pluie : {record.pluie} mm")
        print(f" - Vent moyen : {record.vent_moyen} m/s")
        print(f" - Rafale max : {record.rafale_max} m/s\n")
