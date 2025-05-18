#!/bin/bash

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Running Unit Tests...${NC}"
PYTHONPATH=src pytest tests/unit -v --tb=short --cov=src --cov-report=term-missing

echo -e "\n${YELLOW}Running Integration Tests...${NC}"
PYTHONPATH=src pytest tests/integration -v --tb=short

echo -e "\n${YELLOW}Running Functional Tests...${NC}"
PYTHONPATH=src pytest tests/functional -v --tb=short

# Vérifier la couverture
coverage_minimum=80.0
current_coverage=$(coverage report | tail -n 1 | awk '{print $4}' | tr -d '%')

if (( $(echo "$current_coverage < $coverage_minimum" | bc -l) )); then
    echo -e "${RED}Coverage is below ${coverage_minimum}% (current: ${current_coverage}%)${NC}"
    exit 1
else
    echo -e "${GREEN}Coverage is good: ${current_coverage}%${NC}"
fi
