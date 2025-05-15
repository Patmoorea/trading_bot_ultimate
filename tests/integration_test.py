import unittest
import numpy as np
from src.news_processor.core import NewsSentimentAnalyzer
from src.regime_detection.hmm_kmeans import MarketRegimeDetector

class TestIntegration(unittest.TestCase):
    def test_news_processor(self):
        analyzer = NewsSentimentAnalyzer()
        result = analyzer.analyze(["Bitcoin hits all-time high"])
        self.assertIn("sentiment", result[0])

    def test_regime_detection(self):
        detector = MarketRegimeDetector()
        prices = np.array([100.0, 101.0, 102.0, 101.0, 103.0, 104.0, 103.0, 105.0, 106.0, 107.0])  # 10 valeurs
        detector.fit(prices)
        regime = detector.predict(prices[-5:])  # Utilise les 5 dernières valeurs
        self.assertIn(regime, ["Bull", "Bear", "Sideways"])

if __name__ == "__main__":
    unittest.main()
