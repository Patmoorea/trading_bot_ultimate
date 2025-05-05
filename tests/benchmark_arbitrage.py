import pytest
import asyncio
from unittest.mock import AsyncMock
from modules.arbitrage_engine import ArbitrageEngine

@pytest.fixture
def benchmark_engine():
    engine = ArbitrageEngine()
    engine._process_pair = AsyncMock(return_value={'pair': 'TEST/USD', 'spread': 0.01})
    return engine

@pytest.mark.asyncio
async def test_performance(benchmark_engine, benchmark):
    result = await benchmark(benchmark_engine.check_opportunities_v2)
    assert isinstance(result, list)
