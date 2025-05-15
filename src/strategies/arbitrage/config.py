import os
from dotenv import load_dotenv

load_dotenv()

# Configuration des paires depuis .env
TRADING_PAIRS = os.getenv('TRADING_PAIRS', 'BTC,ETH,SOL,ADA,MATIC,AVAX,LTC,DOGE').split(',')

PAIRS = {
    symbol: {
        'binance': f'{symbol}/USDC',
        'gateio': f'{symbol}/USDT',
        'bingx': f'{symbol}/USDT',
        'okx': f'{symbol}/USDT',
        'blofin': f'{symbol}/USDT'
    }
    for symbol in TRADING_PAIRS
}

# Paramètres de risque depuis .env
SETTINGS = {
    'profit_threshold': 0.003,  # 0.3%
    'max_order_value': float(os.getenv('MAX_POSITION', '0.15')) * 1000,  # 15% du capital
    'min_liquidity': 5000,      # USD
    'fee_adjustment': 1.2,      # Marge de sécurité
    'price_expiry': 5,          # Secondes
    'max_slippage': float(os.getenv('TRAILING_OFFSET', '0.01')),
    'stop_loss': float(os.getenv('STOP_LOSS', '0.05')),
    'take_profit': float(os.getenv('TAKE_PROFIT', '0.15'))
}

FEES = {
    'binance': {'maker': 0.001, 'taker': 0.001},
    'gateio': {'maker': 0.002, 'taker': 0.002},
    'bingx': {'maker': 0.0015, 'taker': 0.0015},
    'okx': {'maker': 0.0008, 'taker': 0.001},
    'blofin': {'maker': 0.0005, 'taker': 0.001}
}
