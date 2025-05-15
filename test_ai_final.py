from src.core_merged.gpu_config import configure_gpu
import numpy as np
from src.core_merged.ai_optimizer_fallback import run_optimization
from src.core_merged.base_model import create_base_model

def main():
    configure_gpu()
    
    print("=== Initialisation ===")
    # Données de test synthétiques
    X_train = np.random.rand(80, 100, 5)
    X_val = np.random.rand(20, 100, 5) 
    y_train = np.random.rand(80, 1)
    y_val = np.random.rand(20, 1)
    
    model = create_base_model(input_shape=(100, 5))

    print("\n=== Début Optimisation ===")
    try:
        params = run_optimization(model, X_train, y_train, X_val, y_val, n_trials=3)
        print("\nMeilleurs paramètres:", params)
    except Exception as e:
        print("\nÉchec optimisation:", str(e))

if __name__ == "__main__":
    main()
