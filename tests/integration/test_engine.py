import pytest
from decimal import Decimal
from src.core.engine import TradingEngine
from src.exchanges.binance.spot_client import BinanceClient

def test_basic_engine_workflow():
    # Setup
    exchange = BinanceClient("test_key", "test_secret")
    engine = TradingEngine([exchange])
    
    # Test initialization
    assert engine.active == True
    assert len(engine.exchanges) == 1
    
    # Test market state
    market_state = engine.get_market_state("BTC/USDT")
    assert "BinanceClient" in market_state
    assert isinstance(market_state["BinanceClient"]["bid"], Decimal)
    
    # Test trade execution
    trade_result = engine.execute_trade({
        "exchange": "BinanceClient",
        "symbol": "BTC/USDT",
        "side": "buy",
        "amount": "0.1",
        "price": "50000"
    })
    assert trade_result["status"] == "open"
    
    # Test shutdown
    engine.stop()
    assert engine.active == False
