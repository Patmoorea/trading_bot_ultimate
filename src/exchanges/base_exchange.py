from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Optional

class BaseExchange(ABC):
    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret
        self._initialize_exchange()

    @abstractmethod
    def _initialize_exchange(self):
        pass

    @abstractmethod
    def get_ticker(self, symbol: str) -> Dict:
        pass

    @abstractmethod
    def get_balance(self) -> Dict:
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, amount: Decimal, 
                   price: Optional[Decimal] = None) -> Dict:
        pass

    @abstractmethod
    def get_order_book(self, symbol: str) -> Dict:
        pass
