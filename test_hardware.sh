#!/bin/zsh
source venv_trading/bin/activate
python -c "
from core.performance import *
from core.monitoring import get_gpu_temp

print('=== TEST COMPLET MATERIEL ===')
optimize_for_m4()
print('Température initiale:', get_gpu_temp(), '°C')

print('\n=== BENCHMARK ===')
duration = benchmark_m4(10000)
print(f'Performance: {duration:.2f}s')

print('\n=== VERIFICATION ===')
print('Résultat vérification:', check_performance_threshold())
"
