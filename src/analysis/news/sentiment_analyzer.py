from transformers import BertForSequenceClassification
from typing import List, Dict

class NewsSentimentEngine:
    """Analyse de sentiment des news cryptos"""
    
    def __init__(self):
        self.model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')
        self.sources = {
            'cryptopanic': {'weight': 0.8},
            'cointelegraph': {'weight': 0.9}
        }
    
    def analyze_headlines(self, headlines: List[str]) -> Dict:
        """Retourne un score de sentiment agrégé"""
        scores = [self.model(h) for h in headlines]
        return {
            'avg_score': sum(scores)/len(scores),
            'positive': sum(s > 0 for s in scores)/len(scores)
        }
