import unittest
from src.arbitrage.cross_exchange import ArbitrageEngine

class TestArbitrage(unittest.TestCase):
    def setUp(self):
        self.engine = ArbitrageEngine()
    
    def test_opportunities(self):
        res = self.engine.find_opportunities('BTC/USDT')
        self.assertIsInstance(res, list)

if __name__ == '__main__':
    unittest.main()
