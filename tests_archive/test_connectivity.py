import asyncio
import ccxt

async def test_exchange(exchange_name):
    try:
        exchange = getattr(ccxt, exchange_name)({
            'enableRateLimit': True,
            'timeout': 5000
        })
        # Test avec une requête simple
        ticker = await exchange.fetch_ticker('BTC/USDT')
        print(f"{exchange_name}: OK - Prix BTC: {ticker['last']}")
        return True
    except Exception as e:
        print(f"{exchange_name}: ÉCHEC - {str(e)}")
        return False

async def main():
    exchanges = ['binance', 'bingx', 'gateio', 'blofin']
    results = await asyncio.gather(*[test_exchange(name) for name in exchanges])
    if not all(results):
        print("\nConseil: Vérifiez votre connexion internet et les restrictions géographiques")

asyncio.run(main())
