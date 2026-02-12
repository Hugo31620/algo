"""
Value object représentant une mesure de température.

Cette classe encapsule une température exprimée en degrés Celsius.
Elle est volontairement simple et utilisée par le modèle Station.
"""


class Temperature:  # pylint: disable=too-few-public-methods
    """
    Représente une mesure de température.

    Cette classe est un value object :
    - elle encapsule uniquement une valeur
    - elle ne contient pas de logique métier
    - elle est utilisée dans le domaine Station
    """

    def __init__(self, value):
        """
        Initialise une mesure de température.

        Args:
            value: température en degrés Celsius (ou None si non disponible)
        """
        self.value = value
