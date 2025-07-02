import numpy as np
import logging

logger = logging.getLogger(__name__)

# Try to import dependencies with fallback
try:
    from hmmlearn import hmm
    from sklearn.cluster import KMeans
    HMM_AVAILABLE = True
except ImportError:
    logger.warning("hmmlearn or sklearn not available, using fallback implementation")
    HMM_AVAILABLE = False


class MarketRegimeDetector:
    def __init__(self, n_regimes=3):
        """Initialize with fallback for missing dependencies"""
        self.n_regimes = n_regimes
        
        if HMM_AVAILABLE:
            self.hmm = hmm.GaussianHMM(n_components=n_regimes)
            self.kmeans = KMeans(n_clusters=n_regimes)
        else:
            self.hmm = None
            self.kmeans = None
            
        self.regimes = {
            0: "Bull",
            1: "Bear", 
            2: "Sideways"
        }
        self.fitted = False

    def fit(self, prices: np.ndarray):
        """Fit the model with fallback implementation"""
        prices = np.array(prices, dtype=np.float64)
        if len(prices) < 10:
            raise ValueError("Au moins 10 prix sont nécessaires pour l'entraînement")
        
        if HMM_AVAILABLE and self.hmm is not None:
            returns = np.log(prices[1:]/prices[:-1])
            self.hmm.fit(returns.reshape(-1, 1))
            self.kmeans.fit(returns.reshape(-1, 1))
        else:
            # Simple fallback - just store the data
            self.price_data = prices
            
        self.fitted = True

    def predict(self, window: np.ndarray) -> str:
        """Predict regime with fallback implementation"""
        window = np.array(window, dtype=np.float64)
        if len(window) < 5:
            return "Insufficient Data"
            
        if HMM_AVAILABLE and self.hmm is not None and self.fitted:
            returns = np.log(window[1:]/window[:-1])
            regime_id = self.hmm.predict(returns.reshape(-1, 1))[-1]
            return self.regimes[regime_id]
        else:
            # Simple fallback based on price movement
            returns = (window[-1] - window[0]) / window[0]
            volatility = np.std(np.diff(window) / window[:-1])
            
            if returns > 0.02 and volatility < 0.05:
                return "Bull"
            elif returns < -0.02 and volatility < 0.05:
                return "Bear"
            else:
                return "Sideways"


class OptimizedMarketRegimeDetector:
    """Version améliorée avec gestion d'erreurs"""
    def __init__(self, n_regimes=3):
        self.n_regimes = n_regimes
        
        if HMM_AVAILABLE:
            self.hmm = hmm.GaussianHMM(
                n_components=n_regimes,
                tol=1e-4,
                n_iter=1000,
                init_params='ste',
                verbose=False
            )
            self.kmeans = KMeans(n_clusters=n_regimes)
        else:
            self.hmm = None
            self.kmeans = None
            
        self.regimes = {
            0: "Bull",
            1: "Bear", 
            2: "Sideways"
        }
        self.fitted = False

    def fit(self, prices: np.ndarray):
        """Fit with enhanced error handling"""
        try:
            prices = np.array(prices, dtype=np.float64)
            if len(prices) < 10:
                raise ValueError("Requiert au moins 10 points de données")
                
            if HMM_AVAILABLE and self.hmm is not None:
                returns = np.log(prices[1:]/prices[:-1])
                self.hmm.fit(returns.reshape(-1, 1))
                self.kmeans.fit(returns.reshape(-1, 1))
            else:
                # Store data for fallback
                self.price_data = prices
                
            self.fitted = True
        except Exception as e:
            logger.error(f"Error fitting regime detector: {e}")
            self.fitted = False

    def predict(self, window: np.ndarray) -> str:
        """Predict with enhanced error handling"""
        try:
            window = np.array(window, dtype=np.float64)
            if len(window) < 5:
                return "Insufficient Data"
                
            if HMM_AVAILABLE and self.hmm is not None and self.fitted:
                returns = np.log(window[1:]/window[:-1])
                regime_id = self.hmm.predict(returns.reshape(-1, 1))[-1]
                return self.regimes[regime_id]
            else:
                # Enhanced fallback
                returns = np.diff(window) / window[:-1]
                mean_return = np.mean(returns)
                volatility = np.std(returns)
                
                if mean_return > 0.01 and volatility < 0.03:
                    return "Bull"
                elif mean_return < -0.01 and volatility < 0.03:
                    return "Bear"
                else:
                    return "Sideways"
        except Exception as e:
            logger.error(f"Error predicting regime: {e}")
            return "Unknown"
