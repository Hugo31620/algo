from src.application.meteo_service import MeteoService
from src.ui.console_view import ConsoleView

if __name__ == "__main__":
    service = MeteoService()
    view = ConsoleView(service)
    view.run()
