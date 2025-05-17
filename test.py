from src.analysis.technical import TechnicalAnalyzer
from src.analysis.technical.advanced import liquidity_wave

# Initialisation
ta = TechnicalAnalyzer()

# Données d'exemple
orderbook_history = [{'ask_volume':10,'bid_volume':5}] * 20

# Calcul des indicateurs
wave = liquidity_wave(orderbook_history)
print("Liquidity Wave:", wave)
