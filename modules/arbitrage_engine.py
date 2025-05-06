import os
import ccxt
from dotenv import load_dotenv
from statistics import mean

load_dotenv()

class ArbitrageEngine:
    def __init__(self):
        self.exchanges = self._init_exchanges()
        self.min_spread = 0.008

    def _init_exchanges(self):
        exchanges = {}
        if os.getenv('BINANCE_API_KEY'):
            exchanges['binance'] = ccxt.binance({
                'apiKey': os.getenv('BINANCE_API_KEY'),
                'secret': os.getenv('BINANCE_API_SECRET'),
                'enableRateLimit': True
            })
        if os.getenv('GATEIO_API_KEY'):
            exchanges['gateio'] = ccxt.gateio({
                'apiKey': os.getenv('GATEIO_API_KEY'),
                'secret': os.getenv('GATEIO_API_SECRET'),
                'enableRateLimit': True
            })
        if os.getenv('BINGX_API_KEY'):
            exchanges['bingx'] = ccxt.bingx({
                'apiKey': os.getenv('BINGX_API_KEY'),
                'secret': os.getenv('BINGX_API_SECRET'),
                'enableRateLimit': True
            })
        return exchanges

    def check_opportunities_v2(self):
        opportunities = []
        for pair in ['BTC/USDC', 'ETH/USDC', 'SOL/USDC']:
            try:
                binance_ask = self.exchanges['binance'].fetch_order_book(pair)['asks'][0][0]
                for name, exchange in self.exchanges.items():
                    if name != 'binance':
                        usdt_pair = pair.replace('USDC', 'USDT')
                        exchange_bid = exchange.fetch_order_book(usdt_pair)['bids'][0][0] * 0.999  # Frais inclus
                        spread = (exchange_bid - binance_ask*1.001) / (binance_ask*1.001)  # Frais inclus
                        if spread > self.min_spread:
                            opportunities.append({
                                'pair': f"{pair}→{usdt_pair}",
                                'spread': spread,
                                'exchange': name
                            })
            except Exception as e:
                print(f"[ERROR] {pair}: {str(e)[:100]}")
        return opportunities

    def find_best_opportunity(self, min_spread=0.0001):
        """Trouve la meilleure opportunité après frais"""
        best = {'spread': 0}
        for pair in ['BTC/USDC', 'ETH/USDC', 'SOL/USDC']:
            try:
                binance_ask = self.exchanges['binance'].fetch_order_book(pair)['asks'][0][0] * 1.001
                for name, exchange in self.exchanges.items():
                    if name == 'binance':
                        continue
                    usdt_pair = pair.replace('USDC', 'USDT')
                    exchange_bid = exchange.fetch_order_book(usdt_pair)['bids'][0][0] * 0.999
                    spread = (exchange_bid - binance_ask) / binance_ask
                    if spread > best['spread'] and spread > min_spread:
                        best = {
                            'pair': pair,
                            'spread': spread,
                            'buy_at': binance_ask/1.001,
                            'sell_at': exchange_bid/0.999,
                            'exchange': name,
                            'profit_%': round(spread*100, 4)
                        }
            except Exception as e:
                print(f"[DEBUG] {pair}: {str(e)[:50]}")
        return best if best['spread'] > 0 else {'status': 'no_opportunity'}

if __name__ == "__main__":
    print("=== ARBITRAGE BOT ===")
    engine = ArbitrageEngine()
    print("Exchanges:", list(engine.exchanges.keys()))
    print("Best Opportunity:", engine.find_best_opportunity())
