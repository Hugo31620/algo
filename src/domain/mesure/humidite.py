"""
Value object représentant une mesure d'humidité.

Cette classe encapsule une valeur d'humidité relative exprimée en pourcentage.
Elle est volontairement simple et immuable.
"""


class Humidite:  # pylint: disable=too-few-public-methods
    """
    Représente une mesure d'humidité relative.

    Cette classe est un value object :
    - elle ne contient pas de logique métier
    - elle encapsule uniquement une valeur
    - elle est utilisée par le domaine Station
    """

    def __init__(self, value):
        """
        Initialise une mesure d'humidité.

        Args:
            value: valeur d'humidité en pourcentage (ou None si non disponible)
        """
        self.value = value
