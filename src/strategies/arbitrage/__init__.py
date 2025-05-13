from .real_arbitrage import USDCArbitrage
from .arbitrage import BaseUSDCArbitrage
from .independent_arbitrage import IndependentUSDCArbitrage

__all__ = ['USDCArbitrage', 'BaseUSDCArbitrage', 'IndependentUSDCArbitrage']

"""
Versions disponibles :
- USDCArbitrage (real_arbitrage.py) - Version par défaut
- BaseUSDCArbitrage (arbitrage.py) - Version basique
- IndependentUSDCArbitrage (independent_arbitrage.py) - Version autonome
"""
