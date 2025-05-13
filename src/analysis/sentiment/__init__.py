from .news_sentiment import NewsSentimentAnalyzer
from .social_sentiment import SocialSentimentAnalyzer

__all__ = ['NewsSentimentAnalyzer', 'SocialSentimentAnalyzer']
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_analysis.log'),
        logging.StreamHandler()
    ]
)
