import asyncio
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class MarketDataCollector:
    def __init__(self, exchange_clients):
        self.exchange_clients = exchange_clients
        self.data_cache = {}
        
    async def fetch_ohlcv(self, exchange, symbol, timeframe, limit=100):
        """
        Récupère les données OHLCV de manière asynchrone
        """
        try:
            ohlcv = await self.exchange_clients[exchange].fetch_ohlcv(
                symbol, timeframe, limit=limit
            )
            
            df = pd.DataFrame(
                ohlcv, 
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            cache_key = f"{exchange}_{symbol}_{timeframe}"
            self.data_cache[cache_key] = df
            
            return df
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données: {str(e)}")

    def get_cached_data(self, exchange, symbol, timeframe):
        """
        Récupère les données du cache
        """
        cache_key = f"{exchange}_{symbol}_{timeframe}"
        return self.data_cache.get(cache_key)

