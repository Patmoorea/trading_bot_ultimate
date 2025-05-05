#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def test_optimization():
    print("=== Testing Optimization ===")
    from src.core.ai_optimizer import run_optimization
    # Mock model for testing
    class MockModel:
        def evaluate(self, _): return [0.5]
        def compile(self, **kwargs): pass
    best_params = run_optimization(MockModel(), n_trials=5)
    print(f"Best params: {best_params}")

def test_rl():
    print("\n=== Testing RL ===")
    from src.core.rl_allocation import CapitalAllocationEnv, train_rl_agent
    env = CapitalAllocationEnv(n_assets=3)
    model = train_rl_agent(env, timesteps=100)
    print("RL test passed")

if __name__ == "__main__":
    test_optimization()
    test_rl()
