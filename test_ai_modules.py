#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test Optuna
print("=== Testing Hyperparameter Optimization ===")
from src.core.ai_optimizer import run_optimization
best_params = run_optimization(base_model=None, n_trials=10)
print(f"Best params: {best_params}")

# Test RL
print("\n=== Testing RL Allocation ===")
from src.core.rl_allocation import CapitalAllocationEnv, train_rl_agent
env = CapitalAllocationEnv(n_assets=5)
model = train_rl_agent(env, timesteps=1000)
print("RL Agent trained successfully")
