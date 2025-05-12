
# ===== INTEGRATION FINBERT =====
from transformers import pipeline

def analyze_with_finbert(text):
    """Extension du module existant"""
    analyzer = pipeline("text-classification", model="yiyanghkust/finbert-tone")
    return analyzer(text)[0]
from transformers import pipeline

def analyze_news(text):
    """Analyse de sentiment avec FinBERT"""
    analyzer = pipeline("text-classification", 
                      model="yiyanghkust/finbert-tone")
    return analyzer(text)[0]['label']

def get_news_impact_score(headline):
    """Extension de l'analyse existante"""
    sentiment = analyze_news(headline)
    return 1.0 if sentiment == 'POSITIVE' else -1.0 if sentiment == 'NEGATIVE' else 0.0
