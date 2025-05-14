from .real_arbitrage import USDCArbitrage
from .arbitrage import BaseUSDCArbitrage
from .independent_arbitrage import IndependentUSDCArbitrage

__all__ = ['USDCArbitrage', 'BaseUSDCArbitrage', 'IndependentUSDCArbitrage']

"""
Versions disponibles :
- USDCArbitrage (real_arbitrage.py) - Version par défaut
- BaseUSDCArbitrage (arbitrage.py) - Version basique
- IndependentUSDCArbitrage (independent_arbitrage.py) - Version autonome
"""

# ============ CONFIGURATION BROKERS ============
BROKER_SETTINGS = {
    'binance': {
        'quote_asset': 'USDC',
        'api_key_env': 'BINANCE_API_KEY',
        'api_secret_env': 'BINANCE_API_SECRET',
        'params': {
            'options': {
                'adjustForTimeDifference': True,
                'defaultType': 'spot'
            }
        }
    },
    'blofin': {
        'quote_asset': 'USDT',
        'api_key_env': 'BLOFIN_API_KEY',
        'api_secret_env': 'BLOFIN_API_SECRET'
    },
    'gateio': {
        'quote_asset': 'USDT',
        'api_key_env': 'GATEIO_API_KEY',
        'api_secret_env': 'GATEIO_API_SECRET'
    },
    'okx': {
        'quote_asset': 'USDT',
        'api_key_env': 'OKX_API_KEY',
        'api_secret_env': 'OKX_API_SECRET',
        'passphrase_env': 'OKX_PASSPHRASE'
    },
    'bingx': {
        'quote_asset': 'USDT',
        'api_key_env': 'BINGX_API_KEY',
        'api_secret_env': 'BINGX_API_SECRET'
    }
}

def convert_pair_to_broker(pair: str, target_broker: str) -> str:
    """Convertit une paire vers le format du broker"""
    base, quote = pair.split('/')
    target_quote = BROKER_SETTINGS.get(target_broker, {}).get('quote_asset', 'USDT')
    
    if quote == target_quote:
        return pair
        
    # Conversion USDC/USDT uniquement
    if {quote, target_quote} == {'USDC', 'USDT'}:
        return f"{base}/{target_quote}"
        
    raise ValueError(f"Conversion non supportée: {pair} -> {target_quote}")
# ============ FIN CONFIGURATION ============

def convert_pair_to_broker(pair: str, target_broker: str) -> str:
    """Version avec logging"""
    import logging
    logger = logging.getLogger(__name__)
    
    base, quote = pair.split('/')
    target_quote = BROKER_SETTINGS.get(target_broker, {}).get('quote_asset', 'USDT')
    
    if quote == target_quote:
        logger.debug(f'Aucune conversion nécessaire pour {pair} sur {target_broker}')
        return pair
        
    if {quote, target_quote} == {'USDC', 'USDT'}:
        new_pair = f"{base}/{target_quote}"
        logger.info(f'Conversion {pair} -> {new_pair} pour {target_broker}')
        return new_pair
        
    raise ValueError(f"Conversion non supportée: {pair} -> {target_quote}")

from functools import lru_cache

@lru_cache(maxsize=100)
def cached_conversion(pair: str, target_broker: str) -> str:
    return convert_pair_to_broker(pair, target_broker)

def validate_quote_assets() -> None:
    """Valide que tous les brokers ont une quote asset USDC ou USDT"""
    valid_quotes = ('USDC', 'USDT')
    for broker, config in BROKER_SETTINGS.items():
        if config.get('quote_asset') not in valid_quotes:
            raise ValueError(
                f"Configuration invalide pour {broker}: "
                f"quote_asset doit être USDC ou USDT (reçu: {config.get('quote_asset')})"
            )
    print("[SUCCESS] Toutes les quotes assets sont valides")

# Validation automatique au chargement
validate_quote_assets()

def validate_quote_assets_with_logging() -> bool:
    """Version avec logging détaillé"""
    import logging
    logger = logging.getLogger(__name__)
    valid = True
    
    for broker, config in BROKER_SETTINGS.items():
        quote = config.get('quote_asset', '')
        if quote not in ('USDC', 'USDT'):
            logger.error(f"Broker {broker} a une quote asset invalide: {quote}")
            valid = False
        else:
            logger.debug(f"Broker {broker} OK - Quote: {quote}")
    
    if valid:
        logger.info("Validation des quotes assets réussie")
    return valid

# Chargement obligatoire du .env
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

# Vérification immédiate
if not os.getenv('BINANCE_API_KEY'):
    raise RuntimeError("La clé Binance n'est pas chargée depuis .env")
