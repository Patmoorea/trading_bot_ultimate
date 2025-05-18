"""
Module d'analyse technique avancé - Created: 2025-05-17 23:06:45
@author: Patmoorea
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class TechnicalAnalyzer:
    def __init__(self):
        self.indicators = {
            'RSI': self._calculate_rsi,
            'MACD': self._calculate_macd,
            'BB': self._calculate_bollinger_bands,
            'ATR': self._calculate_atr
        }
        
    def _calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
        
    def _calculate_macd(self, data: pd.Series) -> Dict[str, pd.Series]:
        exp1 = data.ewm(span=12, adjust=False).mean()
        exp2 = data.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return {'macd': macd, 'signal': signal, 'histogram': macd - signal}
        
    def _calculate_bollinger_bands(self, data: pd.Series, period: int = 20) -> Dict[str, pd.Series]:
        sma = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        return {
            'upper': sma + (std * 2),
            'middle': sma,
            'lower': sma - (std * 2)
        }
        
    def _calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        high_low = high - low
        high_close = (high - close.shift()).abs()
        low_close = (low - close.shift()).abs()
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        return true_range.rolling(window=period).mean()
