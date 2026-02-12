"""
Point d'entrée de l'application météo.

Ce module initialise l'application via la factory
et lance l'interface graphique Tkinter.
"""

from src.application.factory import AppFactory


def main():
    """
    Lance l'application météo.
    """
    app = AppFactory.create_app()
    app.run()


if __name__ == "__main__":
    main()
