#!/bin/bash
# Script de test complet - Created: 2025-05-17 23:06:45
# @author: Patmoorea

echo "🧪 Démarrage des tests..."

# Test des modules principaux
python3 -m pytest tests/strategies -v
python3 -m pytest tests/analysis -v
python3 -m pytest tests/backtesting -v

# Test de l'optimiseur
python3 -m pytest tests/optimization -v

# Test de l'exécuteur d'ordres
python3 -m pytest tests/execution -v

echo "✅ Tests terminés"
