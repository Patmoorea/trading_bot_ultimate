import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD

class IndicatorFusion:
    def __init__(self):
        self.weights = {
            'trend': 0.35,
            'momentum': 0.25,
            'volatility': 0.2,
            'volume': 0.15,
            'orderflow': 0.05
        }
    
    def fuse_indicators(self, data):
        scores = {}
        # Calcul des scores par catégorie
        scores['trend'] = self._calculate_trend_score(data)
        scores['momentum'] = self._calculate_momentum_score(data)
        # ... autres catégories
        
        # Fusion pondérée
        total_score = sum(weight * scores[cat] 
                         for cat, weight in self.weights.items())
        
        return total_score
