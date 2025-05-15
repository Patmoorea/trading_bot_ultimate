"""
Analyse multi-timeframe et volatilité
"""

try:
    from src.core_merged.config import Config
except ImportError:
    class Config:
        USE_NUMBA = False

import pandas as pd
from numba import jit

class MultiTimeframeAnalyzer:
    def __init__(self):
        # Mise à jour des fréquences vers la nouvelle syntaxe
        self.timeframes = ['15min', '1h', '4h', '1D']  

    def analyze(self, data):
        if Config.USE_NUMBA:
            return self._analyze_numba(data)
        return self._analyze_python(data)

    def _analyze_python(self, data):
        """Version Python pure de l'analyse"""
        results = {}
        for tf in self.timeframes:
            try:
                resampled = data.resample(tf).agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last'
                }).dropna()
                results[tf] = resampled
            except Exception as e:
                print(f"Erreur lors du resample {tf}: {str(e)}")
                results[tf] = pd.DataFrame()
        return pd.concat(results, axis=1)

    @jit(nopython=True)
    def _analyze_numba(self, data):
        """Version optimisée avec Numba"""
        # Implémentation alternative si nécessaire
        return {}

class VolatilityAnalyzer:
    def __init__(self, period=14):
        self.period = period

    def calculate_atr(self, df):
        """Calculate Average True Range"""
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift()).abs()
        low_close = (df['low'] - df['close'].shift()).abs()
        true_range = pd.concat(
            [high_low, high_close, low_close], axis=1).max(axis=1)
        return true_range.rolling(self.period).mean()
