class ClassicArbitrage:
    """Implémentation de base de l'arbitrage"""
    
    def calculate(self):
        return {"status": "basic_calculation"}


class ArbitrageEngine:
    """Main arbitrage engine class"""
    
    def __init__(self):
        self.classic_arbitrage = ClassicArbitrage()
    
    def calculate(self):
        """Delegate to classic arbitrage for now"""
        return self.classic_arbitrage.calculate()
