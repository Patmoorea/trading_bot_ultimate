import ccxt.pro as ccxt
import asyncio
import time
from pathlib import Path
import json

class ArbitrageEngine:
    def __init__(self):
        config_path = Path(__file__).parent.parent/'config'/'arbitrage.json'
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.exchanges = self._init_exchanges()
        self.min_spread = self.config['min_spread']

    def _init_exchanges(self):
        exchanges = {}
        for name, params in self.config['exchanges'].items():
            if params['enabled']:
                try:
                    exchange = getattr(ccxt, name)({
                        'enableRateLimit': True,
                        'timeout': params.get('timeout', 10000)
                    })
                    exchanges[name] = exchange
                    print(f'Exchange {name} initialisé')
                except Exception as e:
                    print(f'Erreur initialisation {name}:', str(e))
        return exchanges

    async def check_opportunities_v2(self):
        opportunities = []
        for pair in self.config['whitelist']:
            for exchange_name, exchange in self.exchanges.items():
                try:
                    orderbook = await exchange.watch_order_book(pair)
                    spread = (orderbook['asks'][0][0] - orderbook['bids'][0][0]) / orderbook['asks'][0][0]
                    if spread > self.min_spread:
                        opportunities.append({
                            'exchange': exchange_name,
                            'pair': pair,
                            'spread': spread,
                            'ask': orderbook['asks'][0][0],
                            'bid': orderbook['bids'][0][0],
                            'timestamp': int(time.time())
                        })
                except Exception as e:
                    print(f'Erreur {exchange_name} {pair}:', str(e))
        return opportunities

if __name__ == '__main__':
    async def main():
        engine = ArbitrageEngine()
        opps = await engine.check_opportunities_v2()
        print('Opportunités trouvées:', opps)
    
    asyncio.run(main())
