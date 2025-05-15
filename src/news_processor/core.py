from transformers import BertForSequenceClassification, BertTokenizer
import torch
from typing import List, Dict

class NewsSentimentAnalyzer:
    def __init__(self):
        # Désactive l'optimisation Metal temporairement
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.model = self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
        self.sources = ["coindesk", "reuters", "bloomberg", "cryptopanic"]

    def analyze(self, texts: List[str]) -> List[Dict]:
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return [{
            "text": texts[i],
            "sentiment": "bullish" if torch.argmax(probs[i]).item() == 1 else "bearish",
            "confidence": torch.max(probs[i]).item()
        } for i in range(len(texts))]
