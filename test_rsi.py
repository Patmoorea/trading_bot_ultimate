import numpy as np
import sys
sys.path.append("src/core")  # Ajoute le chemin temporairement

from technical_engine import calculate_rsi_enhanced

test_data = np.array([100,101,102,101,103,104,103,105,104,106,105,107])
print(f"RSI calculé: {calculate_rsi_enhanced(test_data):.2f}")
