import pytest
import sys
import os
from pathlib import Path

# Ajoute le répertoire src au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

@pytest.fixture
def mock_order_book():
    return {
        'bids': [[50000, 1]],
        'asks': [[50500, 1]]
    }

@pytest.fixture
def mock_markets():
    return {
        'BTC/USDC': {'active': True},
        'ETH/USDC': {'active': True}
    }
