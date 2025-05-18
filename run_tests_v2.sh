#!/bin/bash

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Date de l'exécution
EXEC_DATE=$(date '+%Y-%m-%d %H:%M:%S')
echo "Test execution started at: $EXEC_DATE"

echo -e "${YELLOW}Running Unit Tests..."
PYTHONPATH=src pytest tests/unit -v --tb=short --cov=src --cov-report=term-missing

echo -e "\n${YELLOW}Running Integration Tests..."
PYTHONPATH=src pytest tests/integration -v --tb=short

echo -e "\n${YELLOW}Running Performance Tests..."
PYTHONPATH=src pytest tests/performance -v --tb=short

echo -e "\n${YELLOW}Running System Tests..."
PYTHONPATH=src pytest tests/system -v --tb=short

# Vérifier la couverture
coverage_minimum=80.0
current_coverage=$(coverage report | tail -n 1 | awk '{print $4}' | tr -d '%')

if (( $(echo "$current_coverage < $coverage_minimum" | bc -l) )); then
    echo -e "${RED}Coverage is below ${coverage_minimum}% (current: ${current_coverage}%)"
    exit 1
else
    echo -e "${GREEN}Coverage is good: ${current_coverage}%"
fi

# Sauvegarde des résultats
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).log"
{
    echo "Test Results - $EXEC_DATE"
    echo "Coverage: $current_coverage%"
    echo "----------------------------------------"
    coverage report
} > "test_results/$RESULTS_FILE"

echo -e "\n${GREEN}Test results saved to: test_results/$RESULTS_FILE"
