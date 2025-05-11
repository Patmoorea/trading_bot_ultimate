import ccxt
from typing import Dict, List

class ArbitrageEngine:
    EXCHANGES = ['binance', 'kraken', 'ftx', 'huobi', 'coinbase']
    
    def __init__(self):
        self.clients = {ex: getattr(ccxt, ex)() for ex in self.EXCHANGES}
    
    def find_opportunities(self, pair: str) -> List[Dict]:
        prices = {}
        for ex, client in self.clients.items():
            try:
                prices[ex] = client.fetch_ticker(pair)['bid']
            except:
                continue
        return sorted(prices.items(), key=lambda x: x[1])
