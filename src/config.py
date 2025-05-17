class Config:
    # Configuration Numba
    USE_NUMBA = True  # Mettez False si Numba n'est pas installé
    
    # Configuration GPU/CPU
    USE_GPU = True
    
    # Paramètres de trading
    MAX_DRAWDOWN = 0.05
    DAILY_STOP_LOSS = 0.02
    
    # Debug
    DEBUG = False
    LOG_LEVEL = 'INFO'
USE_OPTIMIZED = True  # Passer à False pour désactiver

if USE_OPTIMIZED:
    from src.news_processor.core import CachedNewsSentimentAnalyzer as NewsAnalyzer
    from src.regime_detection.hmm_kmeans import OptimizedMarketRegimeDetector as RegimeDetector
else:
    from src.news_processor.core import NewsSentimentAnalyzer as NewsAnalyzer
    from src.regime_detection.hmm_kmeans import MarketRegimeDetector as RegimeDetector

# Optimisation Apple Silicon
M4_OPTIMIZATION = {
    'tf_device': '/device:apple_m1',  # Compatible M4
    'memory_limit': 12288,  # 12GB pour 16GB RAM
    'use_metal': True
}
