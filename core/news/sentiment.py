from transformers import BertTokenizer, BertForSequenceClassification
import torch

class NewsAnalyzer:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        self.model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
        
    def analyze(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        return torch.softmax(outputs.logits, dim=1).detach().numpy()
