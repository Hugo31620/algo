class Humidite:
    """Représente une humidité relative (en %), avec validation entre 0 et 100."""

    def __init__(self, value: float):
        if not (0 <= value <= 100):
            raise ValueError("L'humidité doit être comprise entre 0 % et 100 %.")
        self.value = f"{value} %"

    def __str__(self):
        return self.value
