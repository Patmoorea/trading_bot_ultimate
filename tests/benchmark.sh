#!/bin/zsh
python -c "
from core.performance import *
print('=== BENCHMARK M4 ===')
results = {
    'small': benchmark_m4(5000),
    'medium': benchmark_m4(10000),
    'large': benchmark_m4(20000)
}
print(f'Résultats: {results}')
assert results['large'] < 10, 'Perf GPU insuffisante'
"
