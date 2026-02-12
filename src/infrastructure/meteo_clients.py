"""
Clients météo (Strategy pattern).

Ce module définit une stratégie d'accès aux données météo (MeteoClient)
et des implémentations concrètes (HTTP réel, mock) afin de découpler
l'application de la source de données.
"""

from __future__ import annotations

from typing import Protocol, Any

from src.infrastructure.api_fetcher import ApiFetcher


class MeteoClient(Protocol):  # pylint: disable=too-few-public-methods
    """
    Interface (port) d'un client météo.

    Une implémentation doit pouvoir récupérer des données brutes depuis
    un endpoint et retourner un objet contenant un attribut .data.
    """

    def fetch(self, endpoint: str) -> Any:
        """
        Récupère les données brutes depuis l'endpoint.

        Args:
            endpoint: URL / identifiant de la source

        Returns:
            Objet contenant les données brutes (ex: RawMeteoData).
        """
        raise NotImplementedError


class HttpMeteoClient:  # pylint: disable=too-few-public-methods
    """
    Implémentation HTTP réelle du client météo.

    Cette classe est volontairement simple et ne gère pas de logique métier.
    """

    def __init__(self, timeout_seconds: int = 10):
        """
        Initialise le client HTTP.

        Args:
            timeout_seconds: délai maximum de la requête HTTP
        """
        self._timeout_seconds = timeout_seconds

    def fetch(self, endpoint: str):
        """
        Appelle l'API via HTTP et retourne les données brutes.

        Args:
            endpoint: URL de l'API

        Returns:
            RawMeteoData: données brutes issues de l'API
        """
        return ApiFetcher(endpoint, timeout_seconds=self._timeout_seconds).fetch()


class MockMeteoClient:  # pylint: disable=too-few-public-methods
    """
    Implémentation mock du client météo.

    Utile pour les tests unitaires ou pour exécuter l'application
    sans accès réseau.
    """

    def __init__(self, payload: Any):
        """
        Initialise le client mock.

        Args:
            payload: objet à retourner lors de fetch()
        """
        self._payload = payload

    def fetch(self, _endpoint: str):
        """
        Retourne le payload fourni au constructeur.

        Args:
            _endpoint: paramètre non utilisé (signature conforme à MeteoClient)

        Returns:
            Payload fourni au constructeur.
        """
        return self._payload
