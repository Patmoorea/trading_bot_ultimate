from binance.spot import Spot
import numpy as np

class SmartOrderRouter:
    def __init__(self, client):
        self.client = client
        
    def get_optimal_price(self, symbol, side, amount):
        ob = self.client.depth(symbol)
        if side == 'BUY':
            return np.min([x[0] for x in ob['asks'][:3]])
        else:
            return np.max([x[0] for x in ob['bids'][:3]])
