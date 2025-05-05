"""
Configuration des exchanges
"""
class BinanceConfig:
    SPOT_API_URL = "https://api.binance.com"
    FUTURES_API_URL = "https://fapi.binance.com"
    TESTNET_URL = "https://testnet.binance.vision"
    
    STREAM_LIMIT = 12
    WS_BUFFER_SIZE = 1000
    RECONNECT_DELAY = 15
