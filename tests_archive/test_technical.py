import pytest
import pandas as pd
from src.core.technical import TechnicalAnalyzer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'close': [100, 101, 102, 103, 104, 105, 104, 103, 102, 101]
    })

def test_rsi_enhanced(sample_data):
    """Test de la méthode calculate_rsi_enhanced"""
    analyzer = TechnicalAnalyzer()
    rsi = analyzer.calculate_rsi_enhanced(sample_data)
    # Vérifie qu'on a des valeurs cohérentes
    assert all(0 <= r <= 100 for r in rsi.dropna())
    assert len(rsi) == len(sample_data)

def test_cache(sample_data):
    """Test du système de cache"""
    analyzer = TechnicalAnalyzer()
    result1 = analyzer.analyze_with_cache(sample_data)
    result2 = analyzer.analyze_with_cache(sample_data)
    assert result1.equals(result2)
