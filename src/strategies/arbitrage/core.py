"""
Configuration spécifique pour Blofin sans passphrase
"""
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor
import ccxt
from concurrent.futures import ThreadPoolExecutorimport logging
from concurrent.futures import ThreadPoolExecutor
load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

class ArbitrageEngine:
    def __init__(self):
        self.brokers = {
            'binance': self._init_exchange('binance'),
            'okx': self._init_exchange('okx', needs_passphrase=True),
            'blofin': self._init_blofin(),  # Méthode spéciale
            'gateio': self._init_exchange('gateio'),
            'bingx': self._init_exchange('bingx')
        }

    def _init_blofin(self):
        """Initialisation spécifique pour Blofin sans passphrase"""
        try:
            return ccxt.blofin({
                'apiKey': os.getenv('BLOFIN_API_KEY'),
                'secret': os.getenv('BLOFIN_API_SECRET'),
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'adjustForTimeDifference': True
                }
            })
        except Exception as e:
            logging.error(f"Erreur initialisation Blofin: {str(e)}")
            raise

    def _init_exchange(self, name: str, needs_passphrase: bool = False):
        """Initialisation standard pour les autres exchanges"""
        # ... (gardez le reste de la méthode existante)

def check_liquidity(self, pair):
    """Nouvelle fonction pour éviter le slippage"""
    binance_depth = self.binance.get_order_book(pair + 'USDC')
    okx_depth = self.okx.get_order_book(pair + 'USDT')
    return {
        'binance': binance_depth['asks'][0][1],
        'okx': okx_depth['bids'][0][1],
        'safe_volume': min(binance_depth['asks'][0][1], okx_depth['bids'][0][1]) * 0.9
    }

def check_liquidity(pair: str) -> dict:
    """Nouvelle fonction safe pour M4"""
    with torch.inference_mode():
        # Implémentation optimisée
        return {...}

def check_liquidity(pair: str) -> dict:
    """Nouvelle fonction safe pour M4"""
    import torch
    with torch.inference_mode():
        return {
            'pair': pair,
            'status': 'implement_this_logic',
            'm4_optimized': True
        }

def _init_blofin(self):
    """Initialisation Blofin optimisée sans passphrase"""
    try:
        exchange = ccxt.blofin({
            'apiKey': os.getenv('BLOFIN_API_KEY'),
            'secret': os.getenv('BLOFIN_API_SECRET'),
            'timeout': 30000,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'fetchMarkets': 'spot',
                'adjustForTimeDifference': True,
                'recvWindow': 10000
            }
        })
        exchange.load_markets()
        return exchange
    except ccxt.AuthenticationError as e:
        logging.critical(f"Erreur auth Blofin: {e}")
        raise
    except ccxt.NetworkError as e:
        logging.warning(f"Erreur réseau Blofin: {e}")
        return None

def check_liquidity(self, pair: str, safe_ratio: float = 0.85) -> dict:
    """Vérification liquidité optimisée M4"""
    import torch
    with torch.inference_mode():
        try:
            binance_symbol = f"{pair}/USDT"
            blofin_symbol = f"{pair}/USD"
            
            with ThreadPoolExecutor() as executor:
                future_binance = executor.submit(
                    self.brokers['binance'].fetch_order_book, 
                    binance_symbol
                )
                future_blofin = executor.submit(
                    self.brokers['blofin'].fetch_order_book,
                    blofin_symbol
                )
                
                binance_book = future_binance.result()
                blofin_book = future_blofin.result()
                
            binance_bid = torch.tensor(binance_book['bids'][0][0])
            binance_ask = torch.tensor(binance_book['asks'][0][0])
            blofin_bid = torch.tensor(blofin_book['bids'][0][0])
            blofin_ask = torch.tensor(blofin_book['asks'][0][0])
            
            spread = (blofin_bid - binance_ask).item()
            safe_volume = min(
                binance_book['asks'][0][1],
                blofin_book['bids'][0][1]
            ) * safe_ratio
            
            return {
                'binance': {
                    'bid': binance_bid.item(),
                    'ask': binance_ask.item(),
                    'safe_volume': safe_volume
                },
                'blofin': {
                    'bid': blofin_bid.item(),
                    'ask': blofin_ask.item(),
                    'safe_volume': safe_volume
                },
                'cross_spread': spread,
                'm4_optimized': torch.backends.mps.is_available()
            }
        except Exception as e:
            logging.error(f"Erreur liquidité {pair}: {str(e)}")
            return {'error': str(e)}

def _calculate_spread_m4(self, bids: list, asks: list) -> float:
    """Calcul optimisé du spread avec M4"""
    import torch
    with torch.inference_mode():
        bids_tensor = torch.tensor([bid[0] for bid in bids])
        asks_tensor = torch.tensor([ask[0] for ask in asks])
        return (torch.max(bids_tensor) - torch.min(asks_tensor)).item()
