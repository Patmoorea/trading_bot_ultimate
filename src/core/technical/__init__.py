import numpy as np
import logging
from typing import Union, Dict, Any
import pandas as pd
from pandas import DataFrame, Series
import pandas_ta as ta

class TechnicalAnalyzer:
    def __init__(self, rsi_length=14):
        self.logger = logging.getLogger(__name__)
        self.rsi_length = rsi_length

    def _ensure_numeric(self, data):
        """Convertit les données en numérique"""
        return pd.to_numeric(data, errors='coerce')

    def calculate_rsi_enhanced(self, df: Union[DataFrame, Series]) -> Series:
        """Version robuste du calcul RSI"""
        try:
            close = self._ensure_numeric(df['close'] if isinstance(df, DataFrame) else df)
            rsi = ta.rsi(close, length=self.rsi_length)
            return rsi.fillna(50)
        except Exception as e:
            self.logger.error(f"Erreur RSI: {str(e)}")
            return Series([50]*len(df), index=df.index)

    def analyze_with_cache(self, df: Union[DataFrame, Series]) -> Dict[str, Any]:
        """Analyse avec cache"""
        from functools import lru_cache
        
        @lru_cache(maxsize=100)
        def cached_rsi(data_tuple):
            data = Series(data_tuple)
            return self.calculate_rsi_enhanced(data.to_frame(name='close'))
            
        close_tuple = tuple(df['close'].values)
        return {'rsi': cached_rsi(close_tuple)}
