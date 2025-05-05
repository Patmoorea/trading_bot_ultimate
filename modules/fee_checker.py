def calculate_net_arbitrage(spread):
    """Prend en compte les frais de trading"""
    fees = {
        'binance': 0.001,  # 0.1%
        'kraken': 0.0016,
        'huobi': 0.002
    }
    return spread - sum(fees.values())
