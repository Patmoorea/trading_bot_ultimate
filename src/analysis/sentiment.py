"""
Analyse de sentiment des news avec adaptation des trades
"""
import requests
from transformers import pipeline
from config import Config


class NewsSentimentAnalyzer:
    def __init__(self):
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="finiteautomata/bertweet-base-sentiment-analysis")
        self.last_news = []

    def fetch_news(self):
        if not Config.NEWS_API_KEY:
            return []

        try:
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "apiKey": Config.NEWS_API_KEY,
                    "q": "crypto OR cryptocurrency",
                    "sources": Config.NEWS_SOURCES,
                    "pageSize": 10
                }
            )
            return response.json().get("articles", [])
        except BaseException:
            return []

    def analyze_news(self):
        articles = self.fetch_news()
        sentiments = []

        for article in articles:
            text = f"{article['title']}. {article['description']}"
            result = self.sentiment_pipeline(text[:512])
            sentiment_score = result[0]['score'] * \
                (1 if result[0]['label'] == 'POS' else -1)
            sentiments.append(sentiment_score)

        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        return avg_sentiment
