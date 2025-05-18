"""
Exchange Manager - Mise à jour: 2025-05-17 23:03:03
@author: Patmoorea
"""
import ccxt
import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

class ExchangeManager:
    def __init__(self):
        self.exchanges: Dict[str, ccxt.Exchange] = {
            'binance': self._init_binance(),
            'gateio': self._init_gateio(),
            'bingx': self._init_bingx(),
            'okx': self._init_okx(),
            'blofin': self._init_blofin()
        }

    def _init_binance(self) -> ccxt.Exchange:
        return ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_API_SECRET'),
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })

    def _init_gateio(self) -> ccxt.Exchange:
        return ccxt.gateio({
            'apiKey': os.getenv('GATEIO_API_KEY'),
            'secret': os.getenv('GATEIO_API_SECRET'),
            'enableRateLimit': True
        })

    def _init_bingx(self) -> ccxt.Exchange:
        return ccxt.bingx({
            'apiKey': os.getenv('BINGX_API_KEY'),
            'secret': os.getenv('BINGX_API_SECRET'),
            'enableRateLimit': True
        })

    def _init_okx(self) -> ccxt.Exchange:
        return ccxt.okx({
            'apiKey': os.getenv('OKX_API_KEY'),
            'secret': os.getenv('OKX_API_SECRET'),
            'password': os.getenv('OKX_PASSPHRASE'),
            'enableRateLimit': True
        })

    def _init_blofin(self) -> ccxt.Exchange:
        return ccxt.blofin({
            'apiKey': os.getenv('BLOFIN_API_KEY'),
            'secret': os.getenv('BLOFIN_API_SECRET'),
            'password': os.getenv('BLOFIN_PASSPHRASE'),
            'enableRateLimit': True
        })

    def get_exchange(self, name: str) -> ccxt.Exchange:
        return self.exchanges.get(name)

    def get_all_exchanges(self) -> Dict[str, ccxt.Exchange]:
        return self.exchanges
