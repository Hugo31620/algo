class ConsoleView:
    """Interface console moderne + navigation station par station."""

    def __init__(self, service):
        self.service = service

    # ---------------------------------------------------------
    #  STYLE MODERNE
    # ---------------------------------------------------------
    def print_box(self, station_name: str, latest):
        print("\n" + "═" * 50)
        print(f"🛰️  Station : {station_name}")
        print("═" * 50)

        print(f"📅 Date/Heure :       {latest.timestamp}")
        print(f"🌡️ Température :      {latest.temperature.value}")
        print(f"💧 Humidité :         {latest.humidite.value}")
        print(f"🔽 Pression :         {latest.pression.value}")
        print(f"☔ Pluie :            {latest.pluie} mm")
        print(f"🌬️ Vent moyen :      {latest.vent_moyen} m/s")
        print(f"💨 Rafale max :       {latest.rafale_max} m/s")

        print("═" * 50 + "\n")

    # ---------------------------------------------------------
    #  BOUCLE PRINCIPALE : LISTE CHAÎNÉE INTERACTIVE
    # ---------------------------------------------------------
    def run(self):
        self.service.load_all_stations()

        # Liste chaînée LOGIQUE : on garde une liste des stations non visitées
        remaining = self.service.get_station_names()

        while remaining:
            print("\nStations restantes :")
            for idx, name in enumerate(remaining, 1):
                print(f"{idx}. {name}")

            try:
                choice = int(input("\n➡️  Choisissez une station : "))
            except ValueError:
                print("❌ Entrée invalide.")
                return

            if not (1 <= choice <= len(remaining)):
                print("❌ Choix invalide.")
                return

            station_name = remaining.pop(choice - 1)  # ❗ On enlève la station choisie

            latest = self.service.get_latest_for_station(station_name)
            if latest is None:
                print("⚠️ Aucune donnée.")
                continue

            # 🔥 Affichage moderne
            self.print_box(station_name, latest)

            # Si plus de station, on s’arrête
            if not remaining:
                print("✔️ Plus aucune station restante. Fin du programme.")
                break

            # Sinon on propose de continuer
            cont = input("➡️  Voulez-vous afficher une autre station ? (o/n) : ")
            if cont.lower() != "o":
                print("👋 Fin du programme.")
                break
