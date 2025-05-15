import os
from decimal import Decimal
from ccxt import binance
from dotenv import load_dotenv

load_dotenv()

class BinanceConnector:
    def __init__(self):
        self.exchange = binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_API_SECRET'),
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True
            },
            'enableRateLimit': True
        })
    
    async def get_order_book(self, symbol: str):
        """Récupère le carnet d'ordres"""
        try:
            orderbook = await self.exchange.fetch_order_book(symbol)
            return Decimal(orderbook['bids'][0][0]), Decimal(orderbook['asks'][0][0])
        except Exception as e:
            raise Exception(f"Erreur Binance: {str(e)}")
    
    async def create_order(self, symbol: str, side: str, amount: Decimal, price: Decimal = None):
        """Crée un ordre"""
        try:
            params = {
                'type': 'market' if not price else 'limit',
                'amount': float(amount),
                'price': float(price) if price else None
            }
            return await self.exchange.create_order(symbol, 'market', side, float(amount), params)
        except Exception as e:
            raise Exception(f"Erreur d'ordre Binance: {str(e)}")
