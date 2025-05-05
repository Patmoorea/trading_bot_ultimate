import requests

class NewsProcessor:
    API_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    def get_crypto_news(self, keywords="crypto OR blockchain"):
        params = {
            'q': keywords,
            'apiKey': self.api_key,
            'pageSize': 5
        }
        try:
            response = requests.get(self.API_URL, params=params)
            return response.json().get('articles', [])
        except Exception as e:
            print(f"Erreur API actualités: {e}")
            return []

def get_news_api_key():
    """Récupère la clé depuis .env de manière sécurisée"""
    from dotenv import load_dotenv
    import os
    load_dotenv()
    return os.getenv('NEWS_API_KEY')

# Version modifiée de la classe
class EnhancedNewsProcessor(NewsProcessor):
    def __init__(self):
        super().__init__(get_news_api_key())
        
    def filter_important_news(self, news):
        """Filtre les news importantes"""
        keywords = ['binance', 'coinbase', 'sec', 'etf', 'fed']
        return [
            n for n in news
            if any(kw in n['title'].lower() for kw in keywords)
        ]
