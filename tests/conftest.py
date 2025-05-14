import pytest
from src.strategies.arbitrage.core import ArbitrageEngine

@pytest.fixture
def arb_engine():
    return ArbitrageEngine(debug_mode=True)
