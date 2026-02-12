"""
Client HTTP chargé de récupérer les données météo depuis l'API distante.

Ce module encapsule l'appel réseau afin d'isoler l'infrastructure
du reste de l'application.
"""

from __future__ import annotations

import requests

from src.domain.mesure.raw_data import RawMeteoData


class ApiFetcher:  # pylint: disable=too-few-public-methods
    """
    Adaptateur HTTP pour la récupération des données météo.

    Cette classe est volontairement simple :
    - une responsabilité unique (appel API)
    - aucune logique métier
    """

    def __init__(self, endpoint: str, timeout_seconds: int = 10):
        """
        Initialise le fetcher HTTP.

        Args:
            endpoint: URL de l'API à interroger
            timeout_seconds: délai maximal de la requête HTTP
        """
        self._endpoint = endpoint
        self._timeout = timeout_seconds

    def fetch(self) -> RawMeteoData:
        """
        Exécute l'appel HTTP et retourne les données brutes.

        Returns:
            RawMeteoData: données météo brutes issues de l'API

        Raises:
            requests.RequestException: en cas d'erreur réseau ou HTTP
        """
        response = requests.get(self._endpoint, timeout=self._timeout)
        response.raise_for_status()

        payload = response.json()

        # API Toulouse Explore v2.1 : données dans "results"
        results = payload.get("results")
        if isinstance(results, list):
            return RawMeteoData(results)

        # Fallback si structure différente
        data = payload.get("data")
        if isinstance(data, list):
            return RawMeteoData(data)

        return RawMeteoData([])
