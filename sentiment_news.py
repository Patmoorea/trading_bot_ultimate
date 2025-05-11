import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime

# Fonction : Récupération des dernières actualités crypto via RSS
def get_crypto_news_rss(max_entries=10):
    feeds = [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cryptopotato.com/feed/"
    ]
    articles = []
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:max_entries]:
            articles.append({
                "title": entry.title,
                "summary": entry.summary if 'summary' in entry else '',
                "published": entry.published,
                "link": entry.link
            })
    return articles

# Fonction : Analyse de sentiment avec VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores['compound']  # Retourne un score entre -1 et 1

# Fonction principale : Sentiment moyen des dernières actualités
def get_overall_sentiment():
    news = get_crypto_news_rss()
    sentiments = []
    for article in news:
        text = article['title'] + " " + article['summary']
        score = analyze_sentiment(text)
        sentiments.append(score)
    if not sentiments:
        return 0.0
    mean_sentiment = sum(sentiments) / len(sentiments)
    return round(mean_sentiment, 3)

# Exemple d'exécution
if __name__ == "__main__":
    sentiment = get_overall_sentiment()
    print(f"[{datetime.datetime.now()}] Sentiment global du marché crypto : {sentiment}")
