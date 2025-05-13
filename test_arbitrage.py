from src.strategies.arbitrage.real_arbitrage import USDCArbitrage

arb = USDCArbitrage(config={'exchanges': ['binance']})
print("Test scan_all_pairs:", arb.scan_all_pairs())
print("Test get_opportunities:", arb.get_opportunities())
arb.switch_broker('binance')
print("Nouveau broker:", arb.exchange)
