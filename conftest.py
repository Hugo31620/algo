"""
Configuration pytest.

Ce fichier ajoute la racine du projet au PYTHONPATH afin de permettre
les imports du package src lors de l'exécution des tests unitaires.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
