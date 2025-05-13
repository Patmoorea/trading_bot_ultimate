import os
import logging
import time
import requests
import torch
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

logger = logging.getLogger(__name__)

class NewsSentimentAnalyzer:
    def __init__(self):
        """Version corrigée pour Apple Silicon"""
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.languages = os.getenv('NEWS_API_LANGUAGES', 'en').split(',')
        self.sources = os.getenv('NEWS_SOURCES', '').split(',')
        self.threshold = float(os.getenv('SENTIMENT_THRESHOLD', 0.7))
        self.refresh_interval = int(os.getenv('NEWS_REFRESH_INTERVAL', 30))
        self.last_fetch = 0
        self.cache = []
        self.sentiment_pipeline = None

        try:
            # Désactiver MPS pour éviter les bugs
            device = "cpu"
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="finiteautomata/bertweet-base-sentiment-analysis",
                device=device,
                framework="pt"
            )
        except Exception as e:
            logger.error(f"Erreur pipeline: {str(e)}")
            self._init_fallback()

    def _init_fallback(self):
        """Initialisation de secours"""
        try:
            from textblob import TextBlob
            self.sentiment_pipeline = "textblob"
            logger.info("Utilisation de TextBlob comme fallback")
        except ImportError:
            logger.error("Aucun analyseur de sentiment disponible")

    # ... [le reste du code reste identique] ...
