from typing import List, Dict
from decimal import Decimal
import asyncio
import logging
from ....exchanges.base_exchange import BaseExchange

class ArbitrageScanner:
    def __init__(self, exchanges: List[BaseExchange], min_profit_threshold: Decimal = Decimal('0.001')):
        self.exchanges = exchanges
        self.min_profit_threshold = min_profit_threshold
        self.logger = logging.getLogger(__name__)

    async def scan_opportunities(self, symbol: str) -> List[Dict]:
        opportunities = []
        try:
            # Récupération des order books
            order_books = await asyncio.gather(
                *[self._get_order_book(exchange, symbol) for exchange in self.exchanges]
            )

            # Analyse des opportunités
            for i, buy_exchange in enumerate(self.exchanges):
                for j, sell_exchange in enumerate(self.exchanges):
                    if i != j:
                        buy_price = order_books[i]['asks'][0][0]
                        sell_price = order_books[j]['bids'][0][0]
                        
                        profit_ratio = (sell_price - buy_price) / buy_price
                        
                        if profit_ratio > self.min_profit_threshold:
                            opportunities.append({
                                'buy_exchange': buy_exchange.__class__.__name__,
                                'sell_exchange': sell_exchange.__class__.__name__,
                                'symbol': symbol,
                                'buy_price': buy_price,
                                'sell_price': sell_price,
                                'profit_ratio': profit_ratio
                            })

        except Exception as e:
            self.logger.error(f"Erreur scan_opportunities: {str(e)}")
            
        return opportunities

    async def _get_order_book(self, exchange: BaseExchange, symbol: str) -> Dict:
        try:
            return await asyncio.to_thread(exchange.get_order_book, symbol)
        except Exception as e:
            self.logger.error(f"Erreur get_order_book pour {exchange.__class__.__name__}: {str(e)}")
            return {'asks': [[Decimal('inf'), Decimal('0')]], 'bids': [[Decimal('0'), Decimal('0')]]}
