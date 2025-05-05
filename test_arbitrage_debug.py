import asyncio
from modules.arbitrage_engine import ArbitrageEngine

async def debug_arbitrage():
    engine = ArbitrageEngine()
    
    # Test avec des paires spécifiques
    test_pairs = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    
    for pair in test_pairs:
        try:
            orderbook = engine.exchange.fetch_order_book(pair)
            spread = (orderbook['asks'][0][0] - orderbook['bids'][0][0]) / orderbook['asks'][0][0]
            print(f"{pair}:")
            print(f"  Ask: {orderbook['asks'][0][0]} | Bid: {orderbook['bids'][0][0]}")
            print(f"  Spread: {spread*100:.4f}% | Min: {engine.min_spread*100:.2f}%")
            print(f"  Eligible: {'OUI' if spread > engine.min_spread else 'NON'}")
        except Exception as e:
            print(f"Erreur sur {pair}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(debug_arbitrage())
