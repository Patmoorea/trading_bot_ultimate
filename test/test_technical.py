import pytest
import pandas as pd
import numpy as np
from src.analysis.technical.technical_analyzer import TechnicalAnalyzer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'open': np.random.uniform(50, 300, 100),
        'high': np.random.uniform(50, 300, 100),
        'low': np.random.uniform(50, 300, 100),
        'close': np.random.uniform(50, 300, 100),
        'volume': np.random.uniform(1000, 5000, 100)
    })

def test_rsi_calculation(sample_data):
    analyzer = TechnicalAnalyzer()
    rsi = analyzer.calculate_rsi(sample_data)
    assert len(rsi) == len(sample_data)
    assert 0 <= rsi.iloc[-1] <= 100

def test_macd_calculation(sample_data):
    analyzer = TechnicalAnalyzer()
    macd = analyzer.calculate_macd(sample_data)
    assert 'macd' in macd
    assert 'signal' in macd
    assert 'histogram' in macd
