"""
Tests d'intégration
"""
import pytest
from src.core_merged.engine import TradingEngine
from config import Config

@pytest.fixture
def engine():
    return TradingEngine()

def test_engine_initialization(engine):
    assert engine is not None
    assert hasattr(engine, 'client')
    assert hasattr(engine, 'technical_analyzer')

def test_market_data_fetching(engine):
    data = engine.get_market_data()
    assert isinstance(data, dict)
