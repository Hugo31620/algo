"""
Factory de création de l'application météo.

Ce module centralise la construction des objets principaux
(service métier, client météo, interface graphique) selon
le pattern Factory.
"""

from src.application.station_directory_service import StationDirectoryService
from src.infrastructure.meteo_clients import HttpMeteoClient
from src.ui.tkinter_app import MeteoApp


class AppFactory:
    """
    Factory responsable de la création et de l'assemblage
    des composants de l'application.
    """

    @staticmethod
    def create_service() -> StationDirectoryService:
        """
        Crée et configure le service principal de gestion des stations météo.

        Returns:
            StationDirectoryService: service configuré avec le client HTTP
            et le cache mémoire.
        """
        client = HttpMeteoClient(timeout_seconds=10)
        return StationDirectoryService(client=client, cache_ttl_seconds=60)

    @staticmethod
    def create_app() -> MeteoApp:
        """
        Crée l'application graphique complète.

        Returns:
            MeteoApp: instance de l'application prête à être lancée.
        """
        service = AppFactory.create_service()
        return MeteoApp(service=service)
