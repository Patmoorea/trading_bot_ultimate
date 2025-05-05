"""
Analyse de sentiment simplifiée sans dépendance lourde
"""
import requests
from config import Config

class NewsSentimentAnalyzer:
    def __init__(self):
        if not Config.NEWS_API_KEY:
            raise ValueError("News API key not configured")

    def fetch_news(self):
        try:
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "apiKey": Config.NEWS_API_KEY,
                    "q": "crypto OR cryptocurrency",
                    "pageSize": 5,
                    "language": "en"
                },
                timeout=10
            )
            articles = response.json().get("articles", [])
            return [a['title'] for a in articles]
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def analyze_sentiment(self, text):
        """Analyse de sentiment simplifiée basée sur des mots-clés"""
        positive_words = ['bullish', 'rise', 'gain', 'up', 'positive']
        negative_words = ['bearish', 'fall', 'drop', 'down', 'negative']
        
        score = 0
        text_lower = text.lower()
        for word in positive_words:
            if word in text_lower:
                score += 0.2
        for word in negative_words:
            if word in text_lower:
                score -= 0.2
                
        return max(-1.0, min(1.0, score))

    def get_market_sentiment(self):
        articles = self.fetch_news()
        if not articles:
            return 0.0
            
        total_score = 0.0
        for article in articles:
            total_score += self.analyze_sentiment(article)
        
        return total_score / len(articles)
