from src.exchanges.base_exchange import BaseExchange
import ccxt
from decimal import Decimal
from typing import Dict, Optional

class GateioSpotClient(BaseExchange):
    def _initialize(self):
        self.exchange = ccxt.gateio({
            'apiKey': self.api_key,
            'secret': self.secret,
            'enableRateLimit': True
        })

    def get_balance(self) -> Dict:
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            self.logger.log_error(f"Erreur balance Gate.io: {str(e)}")
            raise

    def place_order(self, symbol: str, order_type: str, side: str,
                   amount: Decimal, price: Optional[Decimal] = None) -> Dict:
        try:
            return self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=float(amount),
                price=float(price) if price else None
            )
        except Exception as e:
            self.logger.log_error(f"Erreur ordre Gate.io: {str(e)}")
            raise
