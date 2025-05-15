import yaml
from pathlib import Path

def load_pairs_config(config_path: str = 'config/arbitrage_pairs.yaml'):
    """
    Charge la configuration des paires d'arbitrage
    """
    config_file = Path(__file__).parent.parent.parent / config_path
    
    if not config_file.exists():
        raise FileNotFoundError(f"Fichier de configuration {config_path} introuvable")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        
    return config

# Configuration par défaut
DEFAULT_PAIRS = {
    'BTC/USDT': {
        'exchanges': ['binance', 'ftx', 'kraken'],
        'min_volume': 0.1,
        'max_spread': 0.01
    },
    'ETH/USDT': {
        'exchanges': ['binance', 'coinbase', 'kraken'],
        'min_volume': 1.0,
        'max_spread': 0.015
    }
}
