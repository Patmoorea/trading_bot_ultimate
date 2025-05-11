try:
    from modules.news_integration import EnhancedNewsProcessor
    news = EnhancedNewsProcessor()
    print('✓ News Processor:', news.process_news('Test news'))
except Exception as e:
    print(f'⚠️ Error: {str(e)}')
    print('ℹ️ Falling back to basic version...')
    from modules.news_integration import NewsProcessor
    news = NewsProcessor()
    print('✓ Basic News Processor:', news.process_news('Test news'))

from modules.arbitrage_engine import EnhancedArbitrageEngine
engine = EnhancedArbitrageEngine()
print('✓ Arbitrage Fees:', engine.calculate_net_profit(100, 'BTC/USDC'))
