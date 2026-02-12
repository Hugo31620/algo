"""
Value object représentant une mesure de pression atmosphérique.

Cette classe encapsule une pression, généralement exprimée en hPa.
Elle est volontairement simple et utilisée par le modèle Station.
"""


class Pression:  # pylint: disable=too-few-public-methods
    """
    Représente une mesure de pression atmosphérique.

    Cette classe est un value object :
    - elle encapsule uniquement une valeur
    - elle reste volontairement minimale (pas de logique métier complexe)
    """

    def __init__(self, value):
        """
        Initialise une mesure de pression.

        Args:
            value: valeur de pression (hPa) ou None si non disponible
        """
        self.value = value
