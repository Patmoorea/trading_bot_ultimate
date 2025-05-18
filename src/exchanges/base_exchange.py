from abc import ABC, abstractmethod
import ccxt
from decimal import Decimal
from typing import Dict, Optional
from src.utils.logger.trading_logger import TradingLogger

class BaseExchange(ABC):
    def __init__(self, api_key: str, secret: str, password: Optional[str] = None):
        self.api_key = api_key
        self.secret = secret
        self.password = password
        self.logger = TradingLogger(self.__class__.__name__)
        self._initialize()

    @abstractmethod
    def _initialize(self):
        pass

    @abstractmethod
    def get_balance(self) -> Dict:
        pass

    @abstractmethod
    def place_order(self, symbol: str, order_type: str, side: str,
                   amount: Decimal, price: Optional[Decimal] = None) -> Dict:
        pass
