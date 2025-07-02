from transformers import BertForSequenceClassification, BertTokenizer
import torch
from typing import List, Dict, Union
import logging

logger = logging.getLogger(__name__)


class NewsSentimentAnalyzer:
    def __init__(self):
        """Initialize with error handling for model loading"""
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert")
            self.model = self.model.to(self.device)
            self.tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
            self.sources = ["coindesk", "reuters", "bloomberg", "cryptopanic"]
            logger.info("✓ FinBERT model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load FinBERT model: {e}")
            self.model = None
            self.tokenizer = None
            self.device = None
            self.sources = []

    def analyze(self, texts: Union[List[str], str, Dict]) -> List[Dict]:
        """
        Analyze sentiment with improved error handling for different input types
        
        Args:
            texts: Can be List[str], str, or Dict containing text data
            
        Returns:
            List[Dict]: Sentiment analysis results
        """
        try:
            # Handle different input types
            if isinstance(texts, str):
                texts = [texts]
            elif isinstance(texts, dict):
                # Extract text from dict - handle common news API response formats
                if 'text' in texts:
                    texts = [texts['text']]
                elif 'title' in texts:
                    texts = [texts['title']]
                elif 'description' in texts:
                    texts = [texts['description']]
                elif 'content' in texts:
                    texts = [texts['content']]
                else:
                    # Try to find any string values in the dict
                    text_values = [v for v in texts.values() if isinstance(v, str)]
                    texts = text_values if text_values else [""]
            elif not isinstance(texts, list):
                logger.warning(f"Unexpected input type: {type(texts)}, converting to list")
                texts = [str(texts)]
            
            # Filter out empty texts
            texts = [text for text in texts if text and isinstance(text, str)]
            
            if not texts:
                return [{"text": "", "sentiment": "neutral", "confidence": 0.0}]
            
            # If model is not available, return neutral sentiment
            if self.model is None or self.tokenizer is None:
                return [{"text": text, "sentiment": "neutral", "confidence": 0.0} for text in texts]
            
            # Tokenize with error handling
            inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            results = []
            for i in range(len(texts)):
                sentiment_idx = torch.argmax(probs[i]).item()
                confidence = torch.max(probs[i]).item()
                
                # Map FinBERT labels: 0=negative, 1=neutral, 2=positive
                if sentiment_idx == 2:
                    sentiment = "bullish"
                elif sentiment_idx == 0:
                    sentiment = "bearish"
                else:
                    sentiment = "neutral"
                
                results.append({
                    "text": texts[i],
                    "sentiment": sentiment,
                    "confidence": confidence
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            # Return neutral sentiment on error
            fallback_texts = texts if isinstance(texts, list) else [str(texts)]
            return [{"text": text, "sentiment": "neutral", "confidence": 0.0, "error": str(e)} for text in fallback_texts]


class CachedNewsSentimentAnalyzer(NewsSentimentAnalyzer):
    """Version optimisée avec cache local du modèle FinBERT"""
    def __init__(self, model_path: str = "./model_cache/finbert"):
        self.model_path = model_path
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = BertForSequenceClassification.from_pretrained(model_path).to(self.device)
            self.tokenizer = BertTokenizer.from_pretrained(model_path)
            logger.info("✓ Cached FinBERT model loaded")
        except Exception as e:
            logger.warning(f"Cache loading failed ({str(e)}), downloading model...")
            try:
                self.model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert").to(self.device)
                self.tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
                # Try to save for future use
                try:
                    import os
                    os.makedirs(os.path.dirname(model_path), exist_ok=True)
                    self.model.save_pretrained(model_path)
                    self.tokenizer.save_pretrained(model_path)
                    logger.info(f"✓ Model cached to {model_path}")
                except Exception as save_error:
                    logger.warning(f"Could not save model cache: {save_error}")
            except Exception as download_error:
                logger.error(f"Failed to download model: {download_error}")
                self.model = None
                self.tokenizer = None
                
        self.sources = ["coindesk", "reuters", "bloomberg", "cryptopanic"]
