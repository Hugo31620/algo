from src.application.station_directory_service import StationDirectoryService
from src.ui.console_view import ConsoleView

if __name__ == "__main__":
    service = StationDirectoryService()
    view = ConsoleView(service)
    view.run()
