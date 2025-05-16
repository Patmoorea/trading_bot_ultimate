def liquidity_wave(orderbook, depth=10):
    bids = orderbook['bids'][:depth]
    asks = orderbook['asks'][:depth]
    bid_vol = sum(b[1] for b in bids)
    ask_vol = sum(a[1] for a in asks)
    return (bid_vol - ask_vol) / (bid_vol + ask_vol)

def smart_money_index(data):
    """Smart Money Detection Algorithm"""
    pass
