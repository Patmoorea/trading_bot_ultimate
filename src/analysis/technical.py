import numpy as np

class TechnicalAnalyzer:
    """Implémentation parfaite du RSI avec gestion exhaustive des cas"""
    
    def __init__(self):
        self.cache = {'rsi': 50.0, 'macd': 0.0}
    
    def calculate_rsi(self, prices, period=14):
        """
        Calculate RSI with complete edge case handling:
        - Returns 100 when only gains
        - Returns 0 when only losses
        - Returns 50 when no changes or insufficient data
        """
        if len(prices) <= period:
            return 50.0
            
        prices = np.array(prices, dtype=np.float64)
        deltas = np.diff(prices)
        
        gains = np.where(deltas > 0, deltas, 0.0)
        losses = np.where(deltas < 0, -deltas, 0.0)
        
        # Vérification des cas extrêmes avant calcul
        if np.all(gains > 0) and np.all(losses == 0):
            return 100.0
        if np.all(losses > 0) and np.all(gains == 0):
            return 0.0
        if np.all(deltas == 0):
            return 50.0
            
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        if avg_loss == 0:
            return 100.0 if avg_gain > 0 else 50.0
            
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

def calculate_rsi_v2(prices, period=14):
    """Nouvelle implémentation du RSI avec gestion améliorée des cas limites"""
    if len(prices) < period + 1:
        return 50.0
        
    prices = np.array(prices)
    deltas = np.diff(prices)
    
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    
    # Vérification des cas purs avant calcul
    if np.sum(losses) == 0 and np.sum(gains) > 0:
        return 100.0
    if np.sum(gains) == 0 and np.sum(losses) > 0:
        return 0.0
        
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
        
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Ajout de la nouvelle méthode à la classe existante
TechnicalAnalyzer.calculate_rsi_v2 = calculate_rsi_v2
