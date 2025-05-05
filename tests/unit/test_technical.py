import pytest
import pandas as pd
from src.core.technical import TechnicalAnalyzer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105, 104, 103, 102, 101]
    })

def test_rsi_enhanced(sample_data):
    """Test de la méthode calculate_rsi_enhanced existante"""
    analyzer = TechnicalAnalyzer()
    rsi = analyzer.calculate_rsi_enhanced(sample_data)
    assert not rsi.isnull().any()
    assert 0 <= rsi.iloc[-1] <= 100  # RSI doit être entre 0 et 100

def test_cache(sample_data):
    """Test du système de cache avec analyze_with_cache"""
    analyzer = TechnicalAnalyzer()
    result1 = analyzer.analyze_with_cache(sample_data)
    result2 = analyzer.analyze_with_cache(sample_data)
    assert result1['rsi'].equals(result2['rsi'])
