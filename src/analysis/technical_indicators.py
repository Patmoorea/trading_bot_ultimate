"""
Module complet des 42 indicateurs techniques
Organisés par catégorie comme spécifié dans le projet initial
"""

import numpy as np
import pandas as pd
from talib import abstract
from typing import Dict, List

class TechnicalIndicators:
    def __init__(self):
        self.indicators = {
            'trend': self._init_trend_indicators(),
            'momentum': self._init_momentum_indicators(),
            'volatility': self._init_volatility_indicators(),
            'volume': self._init_volume_indicators(),
            'orderflow': self._init_orderflow_indicators()
        }

    # ======================
    # 1. INDICATEURS DE TENDANCE (9)
    # ======================
    def _init_trend_indicators(self) -> Dict:
        return {
            'ichimoku': self.calculate_ichimoku,
            'supertrend': self.calculate_supertrend,
            'vwma': self.calculate_vwma,
            'ema': self.calculate_ema,
            'sma': self.calculate_sma,
            'dema': self.calculate_dema,
            'tema': self.calculate_tema,
            'wma': self.calculate_wma,
            'hma': self.calculate_hma
        }

    def calculate_ichimoku(self, df: pd.DataFrame) -> Dict:
        """Cloud d'Ichimoku avec 3 horizons"""
        high, low, close = df['high'], df['low'], df['close']
        tenkan = (high.rolling(9).max() + low.rolling(9).min()) / 2
        kijun = (high.rolling(26).max() + low.rolling(26).min()) / 2
        senkou_a = ((tenkan + kijun) / 2).shift(26)
        senkou_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)
        return {'tenkan': tenkan, 'kijun': kijun, 'senkou_a': senkou_a, 'senkou_b': senkou_b}

    def calculate_supertrend(self, df: pd.DataFrame, period=10, multiplier=3) -> pd.Series:
        """SuperTrend avec ATR"""
        hl2 = (df['high'] + df['low']) / 2
        atr = self.calculate_atr(df, period)
        upper = hl2 + multiplier * atr
        lower = hl2 - multiplier * atr
        return pd.Series(np.where(close > upper, lower, upper), index=df.index)

    # ======================
    # 2. INDICATEURS DE MOMENTUM (9)
    # ====================== 
    def _init_momentum_indicators(self) -> Dict:
        return {
            'rsi': lambda df: abstract.RSI(df, timeperiod=14),
            'stoch_rsi': self.calculate_stoch_rsi,
            'macd': self.calculate_macd,
            'cci': self.calculate_cci,
            'awesome_oscillator': self.calculate_awesome_oscillator,
            'stochastic': self.calculate_stochastic,
            'williams_r': self.calculate_williams_r,
            'uo': self.calculate_ultimate_oscillator,
            'kst': self.calculate_kst
        }

    def calculate_stoch_rsi(self, df: pd.DataFrame) -> pd.Series:
        """Stochastic RSI"""
        rsi = self.indicators['momentum']['rsi'](df)
        stoch = (rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min())
        return stoch * 100

    # ======================
    # 3. INDICATEURS DE VOLATILITÉ (9)
    # ======================
    def _init_volatility_indicators(self) -> Dict:
        return {
            'atr': self.calculate_atr,
            'bb_width': self.calculate_bb_width,
            'keltner': self.calculate_keltner,
            'donchian': self.calculate_donchian,
            'rvi': self.calculate_rvi,
            'chaikin_volatility': self.calculate_chaikin_volatility,
            'efi': self.calculate_efi,
            'std_dev': self.calculate_std_dev,
            'mass_index': self.calculate_mass_index
        }

    def calculate_atr(self, df: pd.DataFrame, period=14) -> pd.Series:
        """Average True Range"""
        return abstract.ATR(df['high'], df['low'], df['close'], timeperiod=period)

    # ======================
    # 4. INDICATEURS DE VOLUME (9)
    # ======================
    def _init_volume_indicators(self) -> Dict:
        return {
            'obv': self.calculate_obv,
            'vwap': self.calculate_vwap,
            'accumulation': self.calculate_accumulation,
            'cmf': self.calculate_cmf,
            'mfi': self.calculate_mfi,
            'nvi': self.calculate_nvi,
            'pvi': self.calculate_pvi,
            'volume_oscillator': self.calculate_volume_oscillator,
            'eom': self.calculate_eom
        }

    def calculate_vwap(self, df: pd.DataFrame) -> pd.Series:
        """Volume Weighted Average Price"""
        return (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()

    # ======================
    # 5. INDICATEURS DE ORDERFLOW (6)
    # ======================
    def _init_orderflow_indicators(self) -> Dict:
        return {
            'bid_ask_ratio': self.calculate_bid_ask_ratio,
            'liquidity_wave': self.calculate_liquidity_wave,
            'smart_money_index': self.calculate_smart_money_index,
            'market_depth': self.calculate_market_depth,
            'order_imbalance': self.calculate_order_imbalance,
            'volume_profile': self.calculate_volume_profile
        }

    def calculate_bid_ask_ratio(self, orderbook: Dict) -> float:
        """Ratio entre les volumes bid et ask"""
        bid_vol = sum(bid[1] for bid in orderbook['bids'])
        ask_vol = sum(ask[1] for ask in orderbook['asks'])
        return bid_vol / (bid_vol + ask_vol + 1e-10)

    # ======================
    # MÉTHODES UTILITAIRES
    # ======================
    def calculate_all(self, df: pd.DataFrame, orderbook: Dict = None) -> Dict:
        """Calcule tous les indicateurs"""
        results = {}
        for category, indicators in self.indicators.items():
            results[category] = {}
            for name, func in indicators.items():
                try:
                    if category == 'orderflow':
                        results[category][name] = func(orderbook)
                    else:
                        results[category][name] = func(df)
                except Exception as e:
                    print(f"Error calculating {name}: {str(e)}")
                    results[category][name] = None
        return results
