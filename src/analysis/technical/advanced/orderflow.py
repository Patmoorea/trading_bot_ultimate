"""
Module avancé d'analyse du flux d'ordres
"""

import numpy as np
from typing import Dict, List

def smart_money_index(trades: List[Dict], threshold: float = 0.1) -> float:
    """
    Détecte l'activité des 'smart money'
    Retourne: float entre 0 et 1
    """
    large_trades = [t for t in trades if t['amount'] >= threshold]
    if not trades:
        return 0.0
        
    buy_ratio = sum(1 for t in large_trades if t['side'] == 'buy') / len(large_trades)
    freq_ratio = len(large_trades) / len(trades)
    
    return (buy_ratio + freq_ratio) / 2

def market_depth(orderbook: Dict, levels: int = 10) -> Dict:
    """
    Calcule la profondeur de marché sur N niveaux
    Retourne: {'bids': float, 'asks': float}
    """
    bids = sum(bid[1] for bid in orderbook['bids'][:levels])
    asks = sum(ask[1] for ask in orderbook['asks'][:levels])
    return {'bids': bids, 'asks': asks}
