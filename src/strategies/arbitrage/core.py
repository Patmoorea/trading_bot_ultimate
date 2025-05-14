"""
Configuration spécifique pour Blofin sans passphrase
"""
from dotenv import load_dotenv
import os
import ccxt
import logging

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
