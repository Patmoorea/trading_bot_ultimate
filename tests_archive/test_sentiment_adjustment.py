from decision_sentiment_adjustment import adjust_signals_with_sentiment

# Exemples de scores IA bruts simulés
buy = 0.65
sell = 0.35

adjusted_buy, adjusted_sell = adjust_signals_with_sentiment(buy, sell)
print(f"Achat ajusté : {adjusted_buy:.4f}, Vente ajustée : {adjusted_sell:.4f}")
