import finbert_embedding
from transformers import AutoTokenizer

class NewsAnalyzer:
    """Analyse 12 sources avec FinBERT customisé"""
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("finbert")
        self.model = finbert_embedding.FinbertEmbedding()

    def score_impact(self, text):
        return self.model.sentiment(text).mean().item()  # Score 0-1
