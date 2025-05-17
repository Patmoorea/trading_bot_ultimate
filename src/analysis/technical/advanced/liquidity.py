import numpy as np
from typing import List, Dict

def liquidity_wave(orderbook: List[Dict], period: int = 14) -> Dict:
    """
    Version améliorée avec :
    - Normalisation
    - Détection de seuils critiques
    - Gestion des erreurs
    """
    if len(orderbook) < period:
        return {'value': np.nan, 'trend': 'insufficient_data'}
    
    try:
        recent = orderbook[-period:]
        ask_vol = sum(level.get('ask_volume', 0) for level in recent)
        bid_vol = sum(level.get('bid_volume', 0) for level in recent)
        value = (ask_vol - bid_vol) / (ask_vol + bid_vol + 1e-10)
        
        return {
            'value': value,
            'trend': 'bullish' if value > 0.3 else 'bearish' if value < -0.3 else 'neutral',
            'signal': 'extreme' if abs(value) > 0.7 else 'normal'
        }
    except Exception as e:
        return {'error': str(e)}
