#!/bin/bash
clear

echo "=== NETTOYAGE DU CACHE PYTHON ==="
find . -name "*.pyc" -delete
find . -name "__pycache__" -exec rm -rf {} +

echo "=== LANCEMENT DES TESTS ==="
pytest tests/unit/test_technical_analysis.py -v \
  --cov=src/analysis/technical/advanced \
  --cov-report=term-missing \
  --cov-fail-under=80

echo "=== GENERATION DU RAPPORT HTML ==="
pytest --cov=src --cov-report=html

echo "=== VERIFICATION MANUELLE ==="
python -c "
from src.analysis.technical.advanced.liquidity import liquidity_wave
test_data = {
    'normal': ({'bids': [[100,2]], 'asks': [[101,1]]}, 0.3333333),
    'empty': ({'bids': [], 'asks': []}, 'error'),
    'precision': ({'bids': [[100,1.0000001]], 'asks': [[101,1]]}, 0.00000005)
}

for name, (data, expected) in test_data.items():
    try:
        result = liquidity_wave(data)
        assert abs(result - expected) < 1e-6 if name != 'empty' else False
        print(f'✓ {name} test passed')
    except ValueError:
        print(f'✓ {name} test raised expected error')
"
