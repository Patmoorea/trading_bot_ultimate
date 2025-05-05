import asyncio
import websockets
import json
from pandas import DataFrame, Series, read_csv, to_numeric
import logging
from typing import Dict, List
from core.technical_engine import TechnicalEngine

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('realtime_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealTimeBot:
    def __init__(self):
        self.tech_engine = TechnicalEngine()
        self.data_window =  DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        self.window_size = 100

    def _update_data_window(self, new_row: dict):
        """Met à jour la fenêtre de données"""
        new_df =  DataFrame([new_row])
        if self.data_window.empty:
            self.data_window = new_df
        else:
            self.data_window =  concat(
                [self.data_window, new_df],
                ignore_index=True
            ).tail(self.window_size)

    async def handle_socket(self):
        uri = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
        async with websockets.connect(uri) as websocket:
            logger.info("Connecté au flux temps réel Binance")
            while True:
                try:
                    msg = await websocket.recv()
                    data = json.loads(msg)
                    kline = data['k']
                    
                    # Mise à jour des données
                    self._update_data_window({
                        'open': float(kline['o']),
                        'high': float(kline['h']),
                        'low': float(kline['l']),
                        'close': float(kline['c']),
                        'volume': float(kline['v'])
                    })
                    
                    # Analyse technique
                    if len(self.data_window) >= 20:
                        analysis = self.tech_engine.compute(self.data_window)
                        logger.info(f"\nPrix: {self.data_window['close'].iloc[-1]:.2f}")
                        if 'rsi' in analysis.get('momentum', {}):
                            logger.info(f"RSI: {analysis['momentum']['rsi'].iloc[-1]:.2f}")
                
                except json.JSONDecodeError:
                    logger.warning("Erreur de décodage JSON")
                except Exception as e:
                    logger.error(f"Erreur: {str(e)}")

class MultiSymbolRealTimeBot(RealTimeBot):
    def __init__(self, symbols: List[str] = ['btcusdt', 'ethusdt']):
        super().__init__()
        self.symbols = symbols
        self.data_windows = {sym:  DataFrame() for sym in symbols}
        
    async def handle_socket(self):
        streams = [f"{sym}@kline_1m" for sym in self.symbols]
        uri = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
        
        async with websockets.connect(uri) as websocket:
            logger.info(f"Connecté aux symboles: {', '.join(self.symbols)}")
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                stream = data.get('stream')
                
                if stream:
                    symbol = stream.split('@')[0]
                    kline = data['data']['k']
                    self._update_symbol_data(symbol, kline)

    def _update_symbol_data(self, symbol: str, kline: dict):
        """Met à jour les données pour un symbole spécifique"""
        self._update_data_window({
            'symbol': symbol,
            'open': float(kline['o']),
            'high': float(kline['h']),
            'low': float(kline['l']),
            'close': float(kline['c']),
            'volume': float(kline['v'])
        })

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['basic', 'multi'], default='basic')
    parser.add_argument('--symbols', nargs='+', default=['btcusdt'])
    args = parser.parse_args()

    try:
        if args.mode == 'basic':
            bot = RealTimeBot()
        elif args.mode == 'multi':
            bot = MultiSymbolRealTimeBot(args.symbols)
            
        asyncio.get_event_loop().run_until_complete(bot.handle_socket())
    except KeyboardInterrupt:
        logger.info("Arrêt manuel du bot")
    except Exception as e:
        logger.error(f"Erreur critique: {str(e)}")

def start_multi_symbol_engine(symbols):
    """Nouveau moteur multi-symboles avec thread pool"""
    from concurrent.futures import ThreadPoolExecutor
    
    def worker(sym):
        while True:
            try:
                data = fetch_real_time_data(sym)
                processed = process_data(data)
                logger.info(f"{sym} - RSI: {processed['rsi']:.2f}")
            except Exception as e:
                logger.error(f"Error on {sym}: {str(e)}")
                time.sleep(5)
    
    with ThreadPoolExecutor(max_workers=len(symbols)) as executor:
        executor.map(worker, symbols)
