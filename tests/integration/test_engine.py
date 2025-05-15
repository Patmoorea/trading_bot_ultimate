def test_engine_with_ai():
    from src.core_merged.engine import TradingEngine
    engine = TradingEngine()
    assert engine.ai_enabled == False  # Test basique
