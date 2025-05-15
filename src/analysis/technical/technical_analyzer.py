from .indicators import MultiTimeframeAnalyzer, VolatilityAnalyzer
from src.core_merged.config import Config
import pandas as pd

class TechnicalAnalyzer:
    def __init__(self):
        self.multi_tf_analyzer = MultiTimeframeAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
    
    def analyze(self, data):
        """Analyse technique complète"""
        # Vérification de l'index
        if not isinstance(data.index, pd.DatetimeIndex):
            if hasattr(data.index, 'to_datetime'):
                data = data.copy()
                data.index = data.index.to_datetime()
            else:
                raise ValueError("L'index du DataFrame doit être convertible en DatetimeIndex")
        
        tf_analysis = self.multi_tf_analyzer.analyze(data)
        atr = self.volatility_analyzer.calculate_atr(data)
        return {
            'timeframes': tf_analysis,
            'volatility': atr
        }
