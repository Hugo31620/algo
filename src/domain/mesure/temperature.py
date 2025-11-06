class Temperature:
    """Représente une température (en °C), avec validation et formatage."""

    def __init__(self, value: float):
        if not (-100 <= value <= 100):
            raise ValueError("La température doit être comprise entre -100°C et 100°C.")
        self.value = f"{value:.1f} °C"

    def __str__(self):
        return self.value
