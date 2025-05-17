"""
Indicateurs avancés nécessitant des calculs complexes
"""

import numpy as np
from typing import Dict, List

def keltner_channels(high: np.ndarray, low: np.ndarray, close: np.ndarray, 
                   period: int = 20, multiplier: float = 2) -> Dict:
    """Bandes de Keltner avec ATR"""
    typical_price = (high + low + close) / 3
    atr = np.mean(np.abs(high - low))
    middle = np.mean(typical_price[-period:])
    upper = middle + multiplier * atr
    lower = middle - multiplier * atr
    return {'upper': upper, 'middle': middle, 'lower': lower}

def volume_profile(prices: np.ndarray, volumes: np.ndarray, 
                 bins: int = 20) -> Dict:
    """Profil de volume par niveau de prix"""
    hist, bin_edges = np.histogram(prices, bins=bins, weights=volumes)
    return {
        'volume': hist.tolist(),
        'levels': bin_edges[:-1].tolist(),
        'poc': bin_edges[np.argmax(hist)]  # Point of Control
    }
