"""
Module d'analyse du orderflow (flux d'ordres)
Implémente les indicateurs avancés de liquidité
"""

import numpy as np
from typing import List, Dict

def calculate_bid_ask_ratio(orderbook: Dict) -> float:
    """
    Calcule le ratio bid/ask
    Retourne: float entre 0 et 1
    """
    bid_vol = sum([bid[1] for bid in orderbook['bids']])
    ask_vol = sum([ask[1] for ask in orderbook['asks']])
    return bid_vol / (bid_vol + ask_vol + 1e-10)

def calculate_liquidity_wave(orderbook: List[Dict], period: int = 14) -> float:
    """
    Calcule la vague de liquidité sur N périodes
    Formule: (Ask Volume - Bid Volume) / (Ask Volume + Bid Volume)
    Retourne: float entre -1 (bearish) et +1 (bullish)
    """
    if len(orderbook) < period:
        return np.nan
        
    recent = orderbook[-period:]
    ask_vol = sum(level['ask_volume'] for level in recent)
    bid_vol = sum(level['bid_volume'] for level in recent)
    
    return (ask_vol - bid_vol) / (ask_vol + bid_vol + 1e-10)

def calculate_smart_money_index(trades: List[Dict], threshold: float = 0.1) -> float:
    """
    Détecte l'activité des 'smart money'
    Retourne: float entre 0 et 1
    """
    large_trades = [t for t in trades if t['amount'] >= threshold]
    if not trades:
        return 0.0
        
    buy_ratio = sum(1 for t in large_trades if t['side'] == 'buy') / len(large_trades)
    freq_ratio = len(large_trades) / len(trades)
    
    return (buy_ratio + freq_ratio) / 2  # Moyenne des deux métriques

def calculate_market_depth(orderbook: Dict, levels: int = 10) -> Dict:
    """
    Calcule la profondeur de marché sur N niveaux
    Retourne: {'bids': float, 'asks': float}
    """
    bids = sum(bid[1] for bid in orderbook['bids'][:levels])
    asks = sum(ask[1] for ask in orderbook['asks'][:levels])
    return {'bids': bids, 'asks': asks}
