import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def send(self, message):
        if not all([self.token, self.chat_id]):
            print("Configuration Telegram manquante dans .env")
            return False
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        try:
            requests.post(url, data=payload)
            return True
        except Exception as e:
            print(f"Erreur d'envoi Telegram: {str(e)}")
            return False

notifier = TelegramNotifier()
