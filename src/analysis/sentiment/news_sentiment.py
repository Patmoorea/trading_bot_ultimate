import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NewsSentimentAnalyzer:
    def __init__(self):
        self._model = None
        self._tokenizer = None
        self._fallback = SentimentIntensityAnalyzer()
        self._use_mps = False  # Flag pour MPS

    def _init_finbert(self):
        """Initialisation corrigée pour M1/M2/M4"""
        try:
            # Désactiver MPS si problème détecté
            if torch.backends.mps.is_available():
                try:
                    torch.zeros(1).to('mps')  # Test simple
                    self._use_mps = True
                except RuntimeError:
                    print("[INFO] MPS disponible mais buggé - bascule sur CPU")
                    self._use_mps = False

            device = torch.device("mps" if self._use_mps else "cpu")
            model_name = "yiyanghkust/finbert-tone"
            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
            self._model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
            return True
        except Exception as e:
            print(f"[WARNING] FinBERT init failed: {str(e)[:200]}...")  # Truncate long errors
            return False

    def analyze(self, text):
        """Méthode principale avec fallback intelligent"""
        if self._model is None and not self._init_finbert():
            return self._fallback_analyze(text)

        try:
            inputs = self._tokenizer(text, return_tensors="pt").to(self._model.device)
            outputs = self._model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1).tolist()[0]
            return {'finbert': scores}
        except Exception as e:
            print(f"[WARNING] FinBERT analysis failed: {e}")
            return self._fallback_analyze(text)

    def _fallback_analyze(self, text):
        return {'vader': self._fallback.polarity_scores(text)}

def analyze_with_finbert(text):
    return NewsSentimentAnalyzer().analyze(text)

def preload_models():
    """Précharge les modèles au lancement"""
    analyzer = NewsSentimentAnalyzer()
    analyzer._init_finbert()  # Force le chargement initial
    return analyzer
