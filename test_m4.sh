#!/bin/zsh

# Test WebSocket
echo "=== Test WebSocket ==="
python -c "
import asyncio
from src.data_collection.ws_optimized import OptimizedWSClient
async def test():
    client = OptimizedWSClient()
    await client.connect(['wss://stream.binance.com:9443/ws/btcusdt@ticker'])
asyncio.run(test())
"

# Test DecisionEngine Metal
echo "\n=== Test DecisionEngine ==="
python -c "
from src.ai_engine.decision_engine import DecisionEngine
engine = DecisionEngine()
print(engine.make_decision({'close': 50000, 'volume': 1000}))
"

# Test OrderExecutor
echo "\n=== Test OrderExecutor ==="
python src/execution/order_executor.py
