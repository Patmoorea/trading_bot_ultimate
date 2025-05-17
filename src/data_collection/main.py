from ws_optimized import OptimizedWSClient
import asyncio

async def main():
    # Utiliser des URLs valides pour Binance
    client = OptimizedWSClient()
    await client.connect([
        'wss://stream.binance.com:9443/ws/btcusdt@kline_1m',
        'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'
    ])

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Arrêt propre du client WebSocket")
