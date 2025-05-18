import pytest
import sys
import os

# Ajoute le répertoire src au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

@pytest.fixture(autouse=True)
def setup_env():
    """Configure l'environnement pour les tests."""
    os.environ['BINANCE_API_KEY'] = 'test_key'
    os.environ['BINANCE_API_SECRET'] = 'test_secret'
    os.environ['GATEIO_API_KEY'] = 'test_key'
    os.environ['GATEIO_API_SECRET'] = 'test_secret'
    os.environ['BINGX_API_KEY'] = 'test_key'
    os.environ['BINGX_API_SECRET'] = 'test_secret'
    os.environ['OKX_API_KEY'] = 'test_key'
    os.environ['OKX_API_SECRET'] = 'test_secret'
    os.environ['OKX_PASSPHRASE'] = 'test_pass'
    os.environ['BLOFIN_API_KEY'] = 'test_key'
    os.environ['BLOFIN_API_SECRET'] = 'test_secret'
    os.environ['BLOFIN_PASSPHRASE'] = 'test_pass'
    os.environ['ARBITRAGE_THRESHOLD'] = '0.3'
