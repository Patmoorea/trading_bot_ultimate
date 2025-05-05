"""
Analyse technique avec tous les indicateurs demandés
"""
import numpy as np
from pandas import DataFrame, Series, read_csv, to_numeric
from numba import jit
from config import Config

class TechnicalAnalyzer:
    def __init__(self):
        self.indicators = {
            'ichimoku': self.calculate_ichimoku,
            'supertrend': self.calculate_supertrend,
            'vwma': self.calculate_vwma,
            'rsi': self.calculate_rsi,
            'macd': self.calculate_macd,
            'bbands': self.calculate_bbands
        }
    
    @staticmethod
    @jit(nopython=Config.USE_NUMBA)
    def calculate_rsi(prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1.+rs)
        
        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(period-1) + upval)/period
            down = (down*(period-1) + downval)/period
            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)
            
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return {'macd': macd, 'signal': signal_line}
    
    def calculate_ichimoku(self, df):
        high, low, close = df['high'], df['low'], df['close']
        conversion = (high.rolling(9).max() + low.rolling(9).min()) / 2
        base = (high.rolling(26).max() + low.rolling(26).min()) / 2
        lead_a = ((conversion + base) / 2).shift(26)
        lead_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)
        return {'conversion': conversion, 'base': base, 'lead_a': lead_a, 'lead_b': lead_b}
    
    def calculate_supertrend(self, df, period=10, multiplier=3):
        hl2 = (df['high'] + df['low']) / 2
        atr = self.calculate_atr(df, period)
        
        upper = hl2 + (multiplier * atr)
        lower = hl2 - (multiplier * atr)
        
        supertrend =  Series(index=df.index)
        direction =  Series(1, index=df.index)
        
        for i in range(1, len(df)):
            if df['close'][i] > upper[i-1]:
                supertrend[i] = lower[i]
                direction[i] = 1
            elif df['close'][i] < lower[i-1]:
                supertrend[i] = upper[i]
                direction[i] = -1
            else:
                supertrend[i] = supertrend[i-1]
                direction[i] = direction[i-1]
                
        return {'supertrend': supertrend, 'direction': direction}
    
    def calculate_atr(self, df, period=14):
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift()).abs()
        low_close = (df['low'] - df['close'].shift()).abs()
        true_range =  concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return true_range.rolling(period).mean()
    
    def analyze(self, df):
        results = {}
        for name, func in self.indicators.items():
            results[name] = func(df)
        return results
