class ConsoleView:
    """Interface console pour afficher les données météo."""

    def __init__(self, service):
        self.service = service

    def run(self):
        """Boucle principale d'affichage."""
        self.service.load_all_stations()

        stations = self.service.get_station_names()

        print("\nStations météo disponibles :")
        for idx, name in enumerate(stations, 1):
            print(f"{idx}. {name}")

        try:
            choice = int(input("\nChoisissez une station par numéro : "))
        except ValueError:
            print("❌ Entrée invalide.")
            return

        if not (1 <= choice <= len(stations)):
            print("❌ Choix invalide.")
            return

        selected_station = stations[choice - 1]
        print(f"\nDonnées pour la station : {selected_station}\n")

        # 🔥 NOUVELLE MÉTHODE → ON RÉCUPÈRE UNIQUEMENT LA DONNÉE LA PLUS RÉCENTE
        latest = self.service.get_latest_for_station(selected_station)

        if latest is None:
            print("⚠️ Aucune donnée disponible.")
            return

        # 🟦 Affichage formaté
        print(f"Date/Heure : {latest.timestamp}")
        print(f" - Température : {latest.temperature.value}")
        print(f" - Humidité : {latest.humidite.value}")
        print(f" - Pression : {latest.pression.value}")
        print(f" - Pluie : {latest.pluie} mm")
        print(f" - Vent moyen : {latest.vent_moyen} m/s")
        print(f" - Rafale max : {latest.rafale_max} m/s")
