import numpy as np
from hmmlearn import hmm
from sklearn.cluster import KMeans

class MarketRegimeDetector:
    def __init__(self, n_regimes=5):
        self.hmm = hmm.GaussianHMM(n_components=n_regimes)
        self.kmeans = KMeans(n_clusters=n_regimes)
        self.regimes = {
            0: "High Volatility Bull",
            1: "Low Volatility Bull",
            2: "High Volatility Bear", 
            3: "Low Volatility Bear",
            4: "Sideways"
        }

    def fit(self, prices: np.ndarray):
        prices = np.array(prices, dtype=np.float64)  # Conversion explicite
        returns = np.log(prices[1:]/prices[:-1])
        self.hmm.fit(returns.reshape(-1, 1))
        self.kmeans.fit(returns.reshape(-1, 1))

    def predict(self, window: np.ndarray) -> str:
        window = np.array(window, dtype=np.float64)  # Conversion explicite
        returns = np.log(window[1:]/window[:-1])
        regime_id = self.hmm.predict(returns.reshape(-1, 1))[-1]
        return self.regimes[regime_id]
