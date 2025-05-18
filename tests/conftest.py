import pytest
import os
import sys

# Ajout du chemin src au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def setup_test_env():
    # Configuration de l'environnement de test
    os.environ['TESTING'] = 'true'
    os.environ['API_KEY'] = 'test_key'
    os.environ['API_SECRET'] = 'test_secret'
    yield
    # Nettoyage après les tests
    os.environ.pop('TESTING', None)
