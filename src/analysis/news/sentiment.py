from transformers import BertForSequenceClassification
import pandas as pd

class NewsAnalyzer:
    def __init__(self):
        self.model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
        
    def analyze_news(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.logits.softmax(dim=1)
