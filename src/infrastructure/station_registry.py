"""
Registry des stations météo.

Ce module centralise la liste des stations météo de Toulouse Métropole
ainsi que les URLs complètes permettant d'interroger l'API OpenData.
"""

from __future__ import annotations


class StationRegistry:  # pylint: disable=too-few-public-methods
    """
    Registre statique des stations météo.

    Cette classe fournit un point d'accès unique à la liste des stations
    disponibles et à leurs endpoints API associés. Elle est volontairement
    minimale (registry de configuration).
    """

    BASE = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/"

    STATIONS = {
        "Compans-Caffarelli": (
            BASE
            + "42-station-meteo-toulouse-parc-compans-cafarelli/"
            "records?order_by=heure_utc%20desc"
        ),
        "Université Paul Sabatier": (
            BASE
            + "37-station-meteo-toulouse-universite-paul-sabatier/"
            "records?order_by=heure_utc%20desc"
        ),
        "Pech David": (
            BASE
            + "13-station-meteo-toulouse-pech-david/"
            "records?order_by=heure_utc%20desc"
        ),
    }

    @classmethod
    def get_stations(cls) -> dict[str, str]:
        """
        Retourne la liste des stations météo disponibles.

        Returns:
            Dictionnaire associant le nom de la station à son endpoint API.
        """
        return cls.STATIONS
