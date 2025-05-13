import sys
from pathlib import Path

# Mock de BaseModel pour les tests
class BaseModel:
    def __init__(self, config):
        self.config = config

# Injection dans sys.modules
sys.modules['core.base_model'] = type(sys)('core.base_model')
sys.modules['core.base_model'].BaseModel = BaseModel

# Import après mock
from strategies.arbitrage.real_arbitrage import USDCArbitrage

print("=== Test avec mock de BaseModel ===")
arb = USDCArbitrage(config={'exchanges': ['binance']})
print("Opportunités:", arb.get_opportunities())
