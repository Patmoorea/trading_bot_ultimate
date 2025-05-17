#!/bin/bash

# Mode GPU Metal optimisé
export TF_ENABLE_ONEDNN_OPTS=1
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Lancement des services
python src/data_collection/main.py &
python src/ai_engine/decision_engine.py &
python src/execution/order_executor.py &

# Interface Dashboard
streamlit run src/monitoring/dashboard.py
# Chargement des variables d'environnement
export $(grep -v '^#' .env | xargs)

# Lancement des services
python src/data_collection/main.py &
sleep 5  # Attente pour l'initialisation

python src/ai_engine/decision_engine.py &
sleep 3

python src/execution/order_executor.py &
