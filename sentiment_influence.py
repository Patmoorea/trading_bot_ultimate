from sentiment_news import get_overall_sentiment

# Fonction : Biais de sentiment à intégrer dans les signaux du bot
def compute_sentiment_bias():
    score = get_overall_sentiment()
    if score > 0.3:
        return 1.2  # biais haussier
    elif score < -0.3:
        return 0.8  # biais baissier
    else:
        return 1.0  # neutre

# Exemple d'usage
if __name__ == "__main__":
    bias = compute_sentiment_bias()
    print(f"Facteur de biais basé sur le sentiment : {bias}")
