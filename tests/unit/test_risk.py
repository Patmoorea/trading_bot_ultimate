from src.core_merged.risk import RiskManager

def test_max_drawdown():
    rm = RiskManager(max_drawdown=0.05)
    assert rm.calculate_max_position(1000) == 950
