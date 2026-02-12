1. Présentation du projet

Application Python permettant de consulter les données météo en temps réel
des stations de Toulouse Métropole via l’API OpenData officielle.


2. Ouvrir l'application

Ouvrir le terminal et installer les dépendances et tkinter (si non natif à ton python) : 
pip install -r requirements.txt

Ensuite pour lancer l'application: 
python main.py


3. Structure du projet

algodev/
│
├── src/
│   ├── application/      → logique métier (services, factory, event bus)
│   ├── domain/           → modèles et structures de données
│   ├── infrastructure/   → accès API, extraction, mapping
│   └── ui/               → interface graphique Tkinter
│
├── tests/                → tests unitaires
├── main.py               → point d’entrée
└── README.md

Fonctionnalités : 

- Récupération météo en ligne via API Toulouse Métropole
- Affichage température, humidité, pression, vent, pluie
- Historique des consultations
- Mise en cache des données (optimisation)
- Interface graphique simple et ergonomique


4. Implémentation 

- Liste chaînée
Fichier : src/domain/linked_list.py
Utilisée pour stocker l’historique des consultations dans l’interface.

- File
Fichier : src/ui/tkinter_app.py
Utilisée pour gérer les requêtes utilisateur de manière asynchrone (thread worker).

- Dictionnaire
Fichier : src/application/station_directory_service.py
Utilisé pour mettre en cache les données météo déjà récupérées.

Fichier : src/infrastructure/station_registry.py
stocke les stations et leurs URLs API.

5. Design Pattern

- Factory Pattern
Fichier : src/application/factory.py
Permet de créer et configurer l’application et ses dépendances sans couplage direct.

- Strategy Pattern
Fichier : src/infrastructure/meteo_clients.py
Permet de changer la source de données météo : API réelle et mock pour les tests

- Observer Pattern
Fichier : src/application/event_bus.py
Permet de notifier l’interface lorsque les données sont chargées sans bloquer l’application.

6.Respect des principes de conception

SOLID
- Séparation claire des responsabilités (UI / domaine / infrastructure)
- Injection de dépendances (Strategy)
- Classes spécialisées.

KISS
- Logique simple, lisible.
- Pas de complexité inutile.

DRY
- Extraction centralisée des données API (record_extractor.py).

YAGNI
- Pas de fonctionnalités non nécessaires.
- Chaque classe est utilisée.

7. Tests unitaires

Les tests couvrent les structures de données, l’extraction et l’agrégation météo, le service principal, le pattern Observer

Lancer les tests :
pytest -q

8. Respect des normes PEP8

Le code est validé avec pylint. Lancer pylint :
pylint src tests

9. Documentation technique 

Flux de fonctionnement

- L’utilisateur choisit une station.
- La requête est placée dans une file (Queue).
- Un worker récupère les données via l’API.
- Les données sont nettoyées et agrégées.
- Un événement est envoyé à l’interface (Observer).
- L’interface affiche les résultats.
- L’historique est stocké dans la liste chaînée.


Source des données

API OpenData :
https://data.toulouse-metropole.fr

Données publiques, actualisées en temps réel.

