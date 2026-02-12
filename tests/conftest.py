"""
Configuration pytest pour les tests unitaires.

Ce module définit les fixtures communes utilisées par les tests,
notamment des jeux de données simulant les réponses de l'API météo.
"""

import pytest


@pytest.fixture
def sample_records():
    """
    Fournit un ensemble d'enregistrements météo simulés.

    Ces données servent à tester l'extraction et l'agrégation
    des mesures météo indépendamment de l'API réelle.

    Returns:
        Liste de dictionnaires représentant des records météo bruts.
    """
    return [
        {
            "heure_utc": "2026-01-20T10:00:00Z",
            "humidite": 70,
            "pluie": 0.0,
        },
        {
            "heure_utc": "2026-01-20T10:01:00Z",
            "temperature_en_degre_c": 12.3,
        },
        {
            "heure_utc": "2026-01-20T10:02:00Z",
            "pression": 101325,
        },
        {
            "heure_utc": "2026-01-20T10:03:00Z",
            "force_moyenne_du_vecteur_vent": 5.0,
            "direction_du_vecteur_vent_moyen": 180,
        },
    ]
