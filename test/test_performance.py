"""
Tests de performance
"""
import pytest
import time
from src.analysis.technical.technical_analyzer import TechnicalAnalyzer
from test.test_technical import sample_data

@pytest.mark.performance
def test_technical_analysis_performance(sample_data):
    analyzer = TechnicalAnalyzer()
    start_time = time.time()
    
    for _ in range(100):
        analyzer.analyze(sample_data)
    
    elapsed = time.time() - start_time
    assert elapsed < 5.0  # Doit s'exécuter en moins de 5 secondes
