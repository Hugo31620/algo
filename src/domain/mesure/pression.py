class Pression:
    """Représente une pression atmosphérique (en Pa), avec validation."""

    def __init__(self, value: float):
        if value <= 0:
            raise ValueError("La pression doit être un nombre positif.")
        self.value = f"{value:.0f} Pa"

    def __str__(self):
        return self.value
