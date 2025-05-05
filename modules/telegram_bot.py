def send_enhanced_alert(symbol, action, reason, confidence, timeframe, news_link=None):
    message = f"""
    🚨 {action} Signal 🚨
    Pair: {symbol}
    Reason: {reason}
    Confidence: {confidence:.2f}/1.0
    Timeframe: {timeframe}
    """
    if news_link:
        message += f"\n📰 Related News: {news_link}"
    
    bot.send_message(message)
