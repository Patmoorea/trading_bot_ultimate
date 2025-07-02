"""Quantum SVM Module - Enhanced with error handling"""
import logging
import numpy as np
from typing import List, Union

logger = logging.getLogger(__name__)

try:
    from sklearn.svm import SVC
    SKLEARN_AVAILABLE = True
except ImportError:
    logger.warning("sklearn not available for QuantumSVM")
    SKLEARN_AVAILABLE = False


class QuantumSVM:
    def __init__(self):
        """Initialize QuantumSVM with error handling"""
        if SKLEARN_AVAILABLE:
            self.model = SVC(kernel="rbf", gamma=2, probability=True)
            logger.info("QuantumSVM initialized with sklearn backend")
        else:
            self.model = None
            logger.warning("QuantumSVM initialized without sklearn backend")
        self.fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Fit the model with error handling"""
        try:
            X = np.array(X, dtype=float)
            y = np.array(y)
            
            if len(X) == 0 or len(y) == 0:
                logger.warning("Empty training data provided")
                return False
                
            if len(X) != len(y):
                logger.error("Mismatch between X and y dimensions")
                return False
            
            if self.model is not None:
                self.model.fit(X, y)
                self.fitted = True
                logger.info("QuantumSVM fitted successfully")
                return True
            else:
                # Fallback - just store the data
                self.training_data = (X, y)
                self.fitted = True
                logger.info("QuantumSVM fitted (fallback mode)")
                return True
                
        except Exception as e:
            logger.error(f"Error fitting QuantumSVM: {e}")
            self.fitted = False
            return False

    def predict(self, X: np.ndarray) -> Union[np.ndarray, List[float]]:
        """Predict with error handling"""
        try:
            if not self.fitted:
                logger.warning("QuantumSVM not fitted, returning neutral predictions")
                return np.array([0.5] * len(X))
            
            X = np.array(X, dtype=float)
            
            if len(X) == 0:
                return np.array([])
            
            if self.model is not None:
                # Return probability scores for positive class
                probas = self.model.predict_proba(X)
                return probas[:, 1]  # Positive class probabilities
            else:
                # Simple fallback prediction
                predictions = []
                for sample in X:
                    # Simple heuristic based on feature mean
                    mean_val = np.mean(sample) if len(sample) > 0 else 0
                    # Convert to probability-like score
                    score = 1 / (1 + np.exp(-mean_val))  # Sigmoid
                    predictions.append(score)
                return np.array(predictions)
                
        except Exception as e:
            logger.error(f"Error in QuantumSVM prediction: {e}")
            return np.array([0.5] * len(X) if hasattr(X, '__len__') else [0.5])
    
    def predict_proba(self, X: np.ndarray) -> List[List[float]]:
        """Predict class probabilities"""
        try:
            if not self.fitted:
                logger.warning("QuantumSVM not fitted, returning neutral probabilities")
                return [[0.5, 0.5] for _ in range(len(X))]
            
            X = np.array(X, dtype=float)
            
            if len(X) == 0:
                return []
            
            if self.model is not None:
                # Return probability estimates as list
                probas = self.model.predict_proba(X)
                return probas.tolist()
            else:
                # Fallback: convert prediction scores to probabilities
                scores = self.predict(X)
                probas = []
                for score in scores:
                    # Convert score to probability
                    prob_positive = float(score)
                    prob_negative = 1.0 - prob_positive
                    probas.append([prob_negative, prob_positive])
                return probas
                
        except Exception as e:
            logger.error(f"Error in QuantumSVM probability prediction: {e}")
            return [[0.5, 0.5] for _ in range(len(X) if hasattr(X, '__len__') else 1)]
