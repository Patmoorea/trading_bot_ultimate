import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import numpy as np
from core.base_model import create_base_model
from core.ai_optimizer import run_optimization

# Generate synthetic data
X_val = np.random.rand(100, 100, 5)
y_val = np.random.randint(0, 2, 100)

# Test pipeline
model = create_base_model()
print("=== Optimization Start ===")
best_params = run_optimization(
    base_model=model,
    X_val=X_val,
    y_val=y_val,
    n_trials=10
)
print(f"Best params: {best_params}")
