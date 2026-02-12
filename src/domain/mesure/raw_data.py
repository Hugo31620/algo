"""
Conteneur des données météo brutes issues de l'API.

Ce module définit une structure simple permettant de transporter
les données telles que reçues depuis l'API avant tout traitement
ou agrégation.
"""


class RawMeteoData:  # pylint: disable=too-few-public-methods
    """
    Représente un ensemble de données météo brutes.

    Cette classe est volontairement minimale :
    - elle encapsule uniquement les données reçues de l'API
    - elle ne contient aucune logique métier
    - elle sert de DTO entre l'infrastructure et l'application
    """

    def __init__(self, data):
        """
        Initialise les données météo brutes.

        Args:
            data: liste de dictionnaires représentant les enregistrements bruts
        """
        self.data = data
