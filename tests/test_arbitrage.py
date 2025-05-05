import pytest
from unittest.mock import MagicMock, AsyncMock
from src.core.arbitrage import ArbitrageEngine

@pytest.fixture
def mock_engine():
    engine = ArbitrageEngine()
    engine.exchange = MagicMock()
    engine.exchange.fetch_order_book = AsyncMock(return_value={
        'asks': [[100.0, 1.0]], 
        'bids': [[99.0, 1.0]],
        'timestamp': 1234567890
    })
    return engine

@pytest.mark.asyncio
async def test_check_opportunities(mock_engine):
    result = await mock_engine.check_opportunities("BTC/USDT")
    assert 'best_ask' in result
    assert result['spread'] == 1.0
    assert 'timestamp' in result

@pytest.mark.asyncio
async def test_check_opportunities_v2(mock_engine):
    result = await mock_engine.check_opportunities_v2("BTC/USDT")
    assert 'spread_pct' in result
    assert result['liquidity'] == 1.0
    assert 'timestamp' in result
