import ccxt
import os
import time
from dotenv import load_dotenv
from src.utils.telegram_notifications import notifier

load_dotenv()

class EnhancedArbitrage:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not all([self.api_key, self.api_secret]):
            raise ValueError("Configuration Binance manquante dans .env")
            
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True
        })
        self.threshold = float(os.getenv('ARBITRAGE_THRESHOLD', 0.3))

    def check_opportunity(self):
        try:
            usdc = self.exchange.fetch_order_book('BTC/USDC')
            usdt = self.exchange.fetch_order_book('BTC/USDT')
            spread = (usdc['bids'][0][0] / usdt['asks'][0][0] - 1) * 100
            return spread if spread > self.threshold else None
        except Exception as e:
            print(f"Erreur de marché: {str(e)}")
            return None

    def monitor(self):
        print("=== Système d'Arbitrage Activé ===")
        print(f"Seuil: {self.threshold}% | Notifications: {'ON' if os.getenv('TELEGRAM_BOT_TOKEN') else 'OFF'}")
        
        while True:
            spread = self.check_opportunity()
            if spread:
                msg = f"🚨 Arbitrage BTC/USDC-USDT: {spread:.2f}%"
                print(msg)
                if os.getenv('TELEGRAM_BOT_TOKEN'):
                    notifier.send(msg)
            time.sleep(15)
