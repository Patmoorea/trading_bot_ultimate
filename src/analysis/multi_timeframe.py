from pandas import DataFrame, Series, read_csv, to_numeric
import numpy as np

class MultiTimeframeAnalyzer:
    def __init__(self):
        self.timeframes = ['1m', '5m', '15m', '1h']
        
    def resample_data(self, df, timeframe):
        return df.resample(timeframe).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min', 
            'close': 'last',
            'volume': 'sum'
        })
from pandas import DataFrame, Series, read_csv, to_numeric
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class MultiTimeframeAnalyzer:
    def __init__(self):
        self.timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
        
    def compute_indicators(self, data):
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self._process_timeframe, self.timeframes))
        return  concat(results, axis=1)
        
    def _process_timeframe(self, tf):
        # Implémentez ici vos 42 indicateurs
        return  DataFrame({
            f'{tf}_rsi': compute_rsi(data[tf]),
            f'{tf}_macd': compute_macd(data[tf])
        })
