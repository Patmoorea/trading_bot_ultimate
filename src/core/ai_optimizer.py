import optuna
import numpy as np
from tensorflow.keras.models import clone_model

class HyperparameterOptimizer:
    def __init__(self, base_model, X_val, y_val):
        self.base_model = base_model
        self.X_val = X_val
        self.y_val = y_val
        
    def objective(self, trial):
        model = clone_model(self.base_model)
        lr = trial.suggest_float('lr', 1e-5, 1e-2, log=True)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
        history = model.fit(self.X_val, self.y_val, 
                          epochs=1, verbose=0)
        return history.history['loss'][0]

def run_optimization(base_model, X_val, y_val, n_trials=100):
    study = optuna.create_study(direction='minimize')
    optimizer = HyperparameterOptimizer(base_model, X_val, y_val)
    study.optimize(optimizer.objective, n_trials=n_trials)
    return study.best_params
