"""
Configuration centrale optimisée pour M4
"""
import os
import platform
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuration Binance
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    TRADING_PAIRS = [f"{pair.strip()}USDT" for pair in os.getenv("TRADING_PAIRS").split(",")]
    
    # Paramètres de trading
    STOP_LOSS = float(os.getenv("STOP_LOSS", 0.05))
    TAKE_PROFIT = float(os.getenv("TAKE_PROFIT", 0.15))
    TRAILING_OFFSET = float(os.getenv("TRAILING_OFFSET", 0.01))
    
    # News et Sentiment
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    SENTIMENT_THRESHOLD = float(os.getenv("SENTIMENT_THRESHOLD", 0.7))
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Optimisation M4
    IS_M4 = platform.processor() == 'arm' and platform.machine().startswith('arm64')
    USE_METAL = os.getenv("USE_METAL", "true") == "true" and IS_M4
    USE_NUMBA = os.getenv("USE_NUMBA", "true") == "true"
    
    @classmethod
    def validate(cls):
        if not cls.BINANCE_API_KEY or not cls.BINANCE_API_SECRET:
            raise ValueError("Configuration Binance manquante")
