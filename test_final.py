from src.analysis.sentiment import NewsSentimentAnalyzer, analyze_with_finbert

# Test ancienne interface
analyzer = NewsSentimentAnalyzer()
print("Legacy result:", analyzer.analyze("Bitcoin rallies 5%"))

# Test nouvelle interface
print("Direct result:", analyze_with_finbert("Ethereum drops 3%"))
