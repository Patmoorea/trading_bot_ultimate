#!/usr/bin/env python3
import numpy as np
from core import run_optimization, train_rl_agent

# Test Optuna
print("=== Testing Hyperparameter Optimization ===")
best_params = run_optimization(base_model=None, n_trials=10)
print(f"Best params: {best_params}")

# Test RL
print("\n=== Testing RL Allocation ===")
env = CapitalAllocationEnv(n_assets=5)
model = train_rl_agent(env, timesteps=1000)
print("RL Agent trained successfully")
