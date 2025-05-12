from src.strategies.arbitrage.arbitrage_enhanced import EnhancedArbitrage

arb = EnhancedArbitrage()
print("=== TEST ARBITRAGE ===")

try:
    spread = arb.check_opportunity()
    if spread:
        print(f"\033[92mOpportunité détectée: {spread:.4f}%\033[0m")
    else:
        current_spread = (arb.exchange.fetch_order_book('BTC/USDC')['bids'][0][0] / 
                         arb.exchange.fetch_order_book('BTC/USDT')['asks'][0][0] - 1) * 100
        print(f"\033[33mSpread actuel: {current_spread:.4f}% (seuil: {arb.threshold}%)\033[0m")
except Exception as e:
    print(f"\033[91mERREUR: {str(e)}\033[0m")
