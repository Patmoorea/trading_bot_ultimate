import pytest
from src.strategies.arbitrage.arbitrage_enhanced import EnhancedArbitrage

@pytest.fixture
def arb():
    return EnhancedArbitrage()

def test_spread_calculation(arb):
    assert arb.get_current_spread() >= 0  # Le spread ne peut pas être négatif
