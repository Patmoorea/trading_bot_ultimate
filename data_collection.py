
# AJOUT DES 6 NOUVELLES PAIRS USDC
additional_pairs = ['MATICUSDC', 'DOTUSDC', 'AVAXUSDC', 
                   'LINKUSDC', 'ATOMUSDC', 'UNIUSDC']

def init_additional_websockets():
    for pair in additional_pairs:
        ws = WebSocket(f"wss://stream.binance.com:9443/ws/{pair}@trade")
        ws.on_message = lambda msg: process_message(msg)
        ws.start()

# AJOUT DES 6 PAIRS MANQUANTES (USDC)
additional_pairs_usdc = [
    'MATICUSDC', 'AVAXUSDC', 'NEARUSDC',
    'ALGOUSDC', 'FILUSDC', 'ATOMUSDC'
]

def init_additional_websockets():
    """Initialisation des nouveaux flux"""
    for pair in additional_pairs_usdc:
        ws = BinanceWebSocket(pair)
        ws.start()
