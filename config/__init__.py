import os

class Config:
    # Ajout d'une valeur par défaut si TRADING_PAIRS n'est pas défini
    TRADING_PAIRS = os.getenv("TRADING_PAIRS", "BTC,ETH,BNB")
    TRADING_PAIRS = [f"{pair.strip()}USDT" for pair in TRADING_PAIRS.split(",")] if TRADING_PAIRS else []
    
    # Le reste de votre configuration...
