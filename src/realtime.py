import asyncio
import websockets
import json
from pandas import DataFrame, Series, read_csv, to_numeric
from core.technical_engine import TechnicalEngine

class RealTimeBot:
    def __init__(self):
        self.tech_engine = TechnicalEngine()
        
    async def handle_socket(self):
        uri = "wss://stream.binance.com:9443/ws/btcusdc@kline_1m"
        async with websockets.connect(uri) as websocket:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                
                # Création du DataFrame
                df =  DataFrame([{
                    'open': float(data['k']['o']),
                    'high': float(data['k']['h']),
                    'low': float(data['k']['l']),
                    'close': float(data['k']['c']),
                    'volume': float(data['k']['v'])
                }])
                
                # Analyse technique
                analysis = self.tech_engine.compute(df)
                
                # Affichage des résultats
                print("\n=== Nouveau tick ===")
                print(f"Prix: {df['close'].iloc[-1]:.2f}")
                if 'rsi' in analysis['momentum']:
                    print(f"RSI: {analysis['momentum']['rsi'].iloc[-1]:.2f}")

if __name__ == '__main__':
    bot = RealTimeBot()
    asyncio.get_event_loop().run_until_complete(bot.handle_socket())
