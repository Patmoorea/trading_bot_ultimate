#!/usr/bin/env python3
"""
Comprehensive test suite for trading bot fixes
"""
import sys
import os
import logging
import asyncio
import numpy as np
from typing import Dict, List

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_core_modules():
    """Test 1: Core modules import and basic functionality"""
    print("🧪 Test 1: Testing core modules...")
    try:
        from core.technical_engine import TechnicalEngine
        from core.risk_manager import RiskManager
        
        # Test technical engine
        engine = TechnicalEngine()
        test_data = [1.0, 1.1, 1.2, 1.05, 1.3]
        signal = engine.compute(test_data)
        assert isinstance(signal, dict), "Signal should be a dictionary"
        assert 'signal' in signal, "Signal should contain 'signal' key"
        assert 'strength' in signal, "Signal should contain 'strength' key"
        
        # Test risk manager
        risk_mgr = RiskManager()
        risk_assessment = risk_mgr.evaluate_risk(signal)
        assert isinstance(risk_assessment, dict), "Risk assessment should be a dictionary"
        assert 'risk_level' in risk_assessment, "Risk assessment should contain 'risk_level'"
        
        print("✅ Core modules test passed")
        return True
    except Exception as e:
        print(f"❌ Core modules test failed: {e}")
        return False


def test_ai_hybrid_engine():
    """Test 2: AI Hybrid Engine with missing env parameter fix"""
    print("🧪 Test 2: Testing AI Hybrid Engine...")
    try:
        from src.ai.hybrid_engine import HybridEngine
        
        # Test without env parameter (should not fail)
        engine1 = HybridEngine()
        model1 = engine1.build()
        assert model1 is not None, "Model should be created even without env"
        
        # Test with env parameter
        env = {'state_size': 5, 'action_size': 2, 'learning_rate': 0.001}
        engine2 = HybridEngine(env)
        model2 = engine2.build()
        assert model2 is not None, "Model should be created with env"
        
        print("✅ AI Hybrid Engine test passed")
        return True
    except Exception as e:
        print(f"❌ AI Hybrid Engine test failed: {e}")
        return False


def test_sentiment_analysis():
    """Test 3: Sentiment analysis with different input types"""
    print("🧪 Test 3: Testing sentiment analysis...")
    try:
        from src.news_processor.core import NewsSentimentAnalyzer
        
        analyzer = NewsSentimentAnalyzer()
        
        # Test with list of strings
        result1 = analyzer.analyze(["Bitcoin price is rising"])
        assert isinstance(result1, list), "Result should be a list"
        assert len(result1) > 0, "Result should not be empty"
        assert 'sentiment' in result1[0], "Result should contain sentiment"
        
        # Test with single string
        result2 = analyzer.analyze("Bitcoin market is volatile")
        assert isinstance(result2, list), "Result should be a list"
        assert len(result2) == 1, "Result should have one item for single string"
        
        # Test with dict (simulating API response format)
        api_response = {'title': 'Bitcoin news', 'content': 'Market update'}
        result3 = analyzer.analyze(api_response)
        assert isinstance(result3, list), "Result should be a list"
        assert len(result3) > 0, "Result should not be empty"
        
        # Test with empty input
        result4 = analyzer.analyze([])
        assert isinstance(result4, list), "Result should be a list"
        
        print("✅ Sentiment analysis test passed")
        return True
    except Exception as e:
        print(f"❌ Sentiment analysis test failed: {e}")
        return False


def test_news_fetcher():
    """Test 4: News fetcher error handling"""
    print("🧪 Test 4: Testing news fetcher...")
    try:
        from src.news.enhanced_fetcher import EnhancedNewsFetcher, fetch_all_news
        
        # Test async news fetching (won't get real data but should handle errors gracefully)
        async def run_test():
            news = await fetch_all_news()
            assert isinstance(news, list), "News should be a list"
            return True
        
        result = asyncio.run(run_test())
        
        print("✅ News fetcher test passed")
        return True
    except Exception as e:
        print(f"❌ News fetcher test failed: {e}")
        return False


def test_regime_detection():
    """Test 5: Market regime detection with fallback"""
    print("🧪 Test 5: Testing market regime detection...")
    try:
        from src.regime_detection.hmm_kmeans import MarketRegimeDetector, OptimizedMarketRegimeDetector
        
        # Test basic detector
        detector1 = MarketRegimeDetector()
        
        # Test with sufficient data
        price_data = np.array([100, 101, 102, 101, 103, 104, 102, 105, 106, 107, 108])
        detector1.fit(price_data)
        regime = detector1.predict(price_data[-5:])
        assert isinstance(regime, str), "Regime should be a string"
        
        # Test optimized detector
        detector2 = OptimizedMarketRegimeDetector()
        detector2.fit(price_data)
        regime2 = detector2.predict(price_data[-5:])
        assert isinstance(regime2, str), "Regime should be a string"
        
        # Test with insufficient data
        regime3 = detector1.predict([100, 101])
        assert regime3 == "Insufficient Data", "Should handle insufficient data"
        
        print("✅ Market regime detection test passed")
        return True
    except Exception as e:
        print(f"❌ Market regime detection test failed: {e}")
        return False


def test_quantum_svm():
    """Test 6: Quantum SVM with fallback implementation"""
    print("🧪 Test 6: Testing Quantum SVM...")
    try:
        from src.quantum_ml.qsvm import QuantumSVM
        
        qsvm = QuantumSVM()
        
        # Test fitting
        X = np.array([[1, 2], [2, 3], [3, 1], [4, 2]])
        y = np.array([0, 1, 0, 1])
        
        fit_success = qsvm.fit(X, y)
        assert fit_success, "Fitting should succeed"
        
        # Test prediction
        X_test = np.array([[1.5, 2.5], [3.5, 1.5]])
        predictions = qsvm.predict(X_test)
        assert isinstance(predictions, (list, np.ndarray)), "Predictions should be list or array"
        assert len(predictions) == len(X_test), "Predictions length should match input"
        
        # Test probability prediction
        probas = qsvm.predict_proba(X_test)
        assert isinstance(probas, list), "Probabilities should be a list"
        assert len(probas) == len(X_test), "Probabilities length should match input"
        
        print("✅ Quantum SVM test passed")
        return True
    except Exception as e:
        print(f"❌ Quantum SVM test failed: {e}")
        return False


def test_liquidity_heatmap():
    """Test 7: Liquidity heatmap generation"""
    print("🧪 Test 7: Testing liquidity heatmap...")
    try:
        from src.liquidity_heatmap.visualization import generate_heatmap, visualize_heatmap_text
        
        # Test with valid orderbook
        orderbook = {
            'bids': [[50000, 1.5], [49950, 2.0], [49900, 1.8]],
            'asks': [[50100, 1.2], [50150, 1.7], [50200, 2.1]]
        }
        
        heatmap = generate_heatmap(orderbook)
        assert isinstance(heatmap, dict), "Heatmap should be a dictionary"
        assert 'status' in heatmap, "Heatmap should have status"
        assert 'bid_levels' in heatmap, "Heatmap should have bid_levels"
        assert 'ask_levels' in heatmap, "Heatmap should have ask_levels"
        
        # Test visualization
        text_viz = visualize_heatmap_text(heatmap)
        assert isinstance(text_viz, str), "Visualization should be a string"
        
        # Test with invalid orderbook
        invalid_orderbook = None
        heatmap_invalid = generate_heatmap(invalid_orderbook)
        assert heatmap_invalid['status'] == 'error', "Should handle invalid orderbook"
        
        print("✅ Liquidity heatmap test passed")
        return True
    except Exception as e:
        print(f"❌ Liquidity heatmap test failed: {e}")
        return False


def test_main_bot_integration():
    """Test 8: Main bot integration"""
    print("🧪 Test 8: Testing main bot integration...")
    try:
        # Import and test the main trading bot
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
        
        # This should work without errors
        import main
        
        print("✅ Main bot integration test passed")
        return True
    except Exception as e:
        print(f"❌ Main bot integration test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("🚀 Running Trading Bot Fix Validation Tests")
    print("=" * 60)
    
    tests = [
        test_core_modules,
        test_ai_hybrid_engine,
        test_sentiment_analysis,
        test_news_fetcher,
        test_regime_detection,
        test_quantum_svm,
        test_liquidity_heatmap,
        test_main_bot_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Trading bot fixes are working correctly.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Some issues may remain.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)