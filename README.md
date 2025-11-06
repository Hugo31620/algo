1. Domaine métier (le cœur logique)
C’est la partie qui représente la réalité du terrain : les villes, les stations météo et les relevés météo.

Meteo_Ville : représente la météo globale pour toutes les villes gérées par l'application.

Nom_Station : groupe de stations météo dans une ville donnée (par ex. : les stations de métro de Toulouse).

Station : une véritable station météo, avec sa position GPS et ses mesures.

Temperature, Humidite, Pression : objets qui contiennent une mesure précise (pour éviter les erreurs et garder un code propre).


2. Accès aux données (Infrastructure)
Cette partie sert à aller chercher les données météo en dehors du programme.

Api_Fetcher : récupère les données brutes en appelant l’API Open Data Toulouse.

Meteo_Mapper : transforme ces données brutes en objets Python prêts à être utilisés.

Dataset_Documentation : génère une compréhension claire des données (statistiques, rapport...).


3. Logique applicative (Services)
Ce sont les étapes concrètes du traitement que l’application doit faire.

Meteo_Service : le chef d’orchestre. Récupère les données → les organise → et les envoie à l’affichage.

Data_Cleaner : "nettoie" ou prépare les données si besoin (ex : convertir des chaînes en nombres).

Station_Selector : permet de choisir quelle station afficher.



4. Interface utilisateur (UI)
C’est la sortie visible pour l’utilisateur.

Console_View : affiche le résultat directement dans le terminal, et permet de naviguer entre les stations.



En résumé : comment ça marche ?
API → Api_Fetcher → Meteo_Mapper → Domaine (ex : Station)
     → Meteo_Service → Console_View → Affichage à l’utilisateur

algodev/
│
├── src/
│   ├── domain/                  # Entités métier + Value Objects
│   │   ├── meteo.py
│   │   ├── station.py
│   │   ├── ville.py
│   │   └── mesure/
│   │       ├── temperature.py
│   │       ├── humidite.py
│   │       └── pression.py
│   │       └── raw_data.py
│   │
│   ├── infrastructure/          # API, mapping, dataset profiling
│   │   ├── api_fetcher.py
│   │   ├── meteo_mapper.py
│   │   └── dataset_documentation.py
│   │
│   ├── application/             # Services / orchestrations
│   │   ├── meteo_service.py
│   │   ├── data_cleaner.py
│   │   └── station_selector.py
│   │
│   └── ui/                      # Interface utilisateur
│       └── console_view.py
│
├── tests/
├── docs/
│   └── uml.png
├── main.py
├── requirements.txt
└── README.md
