import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

class ArbitrageEngine:
    def __init__(self):
        self.exchanges = self._init_exchanges()
        self.min_spread = 0.001
        self.min_volume = 0.001

    def _init_exchanges(self):
        exchanges = {}
        
        # Binance
        if os.getenv('BINANCE_API_KEY'):
            exchanges['binance'] = ccxt.binance({
                'apiKey': os.getenv('BINANCE_API_KEY'),
                'secret': os.getenv('BINANCE_API_SECRET')
            })
        
        # OKX
        if os.getenv('OKX_API_KEY'):
            exchanges['okx'] = ccxt.okx({
                'apiKey': os.getenv('OKX_API_KEY'),
                'secret': os.getenv('OKX_API_SECRET'),
                'password': os.getenv('OKX_PASSPHRASE')
            })

        # Configuration commune
        for exchange in exchanges.values():
            exchange.enableRateLimit = True
        return exchanges

    def validate_config(self):
        """Vérifie la connexion et les balances"""
        print("\n=== VALIDATION ===")
        for name, exchange in self.exchanges.items():
            try:
                ticker = exchange.fetch_ticker('BTC/USDT' if name != 'binance' else 'BTC/USDC')
                balance = exchange.fetch_free_balance()
                print(f"{name}:")
                print(f"  Dernier prix BTC: {ticker['last']:.2f}")
                print(f"  Balance disponible: {balance.get('USDT', balance.get('USDC', 0)):.2f} USD")
            except Exception as e:
                print(f"{name}: ERROR - {str(e)[:100]}")

if __name__ == "__main__":
    engine = ArbitrageEngine()
    engine.validate_config()
