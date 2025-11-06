class RawMeteoData:
    """Stocke les données brutes reçues depuis l'API."""

    def __init__(self, data: list):
        self.data = data

    def __repr__(self):
        return f"RawMeteoData({len(self.data)} entrées)"
