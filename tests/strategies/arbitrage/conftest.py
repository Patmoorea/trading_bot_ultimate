import pytest
from strategies.arbitrage.cross_exchange import CrossExchangeArbitrage

@pytest.fixture
def arbitrage_engine():
    return CrossExchangeArbitrage(exchanges=['binance', 'kraken'])
