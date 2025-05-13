
    def execute_trade(self, pair: str, amount: float) -> bool:
        """Exemple de méthode à implémenter"""
        print(f"EXÉCUTION SIMULÉE: {amount} {pair}")
        return True

    def get_liquidity(self, pair: str) -> float:
        """Nouvelle méthode pour analyser la liquidité"""
        # Implémentation à compléter
        return 0.0

# ============ NOUVELLE CONFIGURATION MULTI-BROKER ============
BROKER_CONFIG = {
    'binance': {
        'quote_asset': 'USDC',
        'api_key_env': 'BINANCE_API_KEY',
        'api_secret_env': 'BINANCE_API_SECRET',
        'special_params': {'options': {'adjustForTimeDifference': True}}
    },
    'gateio': {
        'quote_asset': 'USDT', 
        'api_key_env': 'GATEIO_API_KEY',
        'api_secret_env': 'GATEIO_API_SECRET'
    },
    'bingx': {
        'quote_asset': 'USDT',
        'api_key_env': 'BINGX_API_KEY',
        'api_secret_env': 'BINGX_API_SECRET'
    },
    'blofin': {
        'quote_asset': 'USDT',
        'api_key_env': 'BLOFIN_API_KEY',
        'api_secret_env': 'BLOFIN_API_SECRET'
    },
    'okx': {
        'quote_asset': 'USDT',
        'api_key_env': 'OKX_API_KEY',
        'api_secret_env': 'OKX_API_SECRET',
        'requires_passphrase': True,
        'passphrase_env': 'OKX_PASSPHRASE'
    }
}

class MultiBrokerArbitrage:
    """Nouvelle classe pour gérer les 5 brokers sans modifier l'existant"""
    def __init__(self):
        self.brokers = {}
        for broker_name, config in BROKER_CONFIG.items():
            self._init_broker(broker_name, config)
    
    def _init_broker(self, broker_name, config):
        """Initialisation sécurisée d'un broker"""
        try:
            exchange_class = getattr(ccxt, broker_name)
            params = {
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'}
            }
            
            # Ajout des paramètres spécifiques
            if config.get('special_params'):
                params.update(config['special_params'])
                
            # Configuration des clés API
            api_key = os.getenv(config['api_key_env'])
            api_secret = os.getenv(config['api_secret_env'])
            
            if api_key and api_secret:
                params.update({
                    'apiKey': api_key,
                    'secret': api_secret
                })
                
                if config.get('requires_passphrase'):
                    params['password'] = os.getenv(config['passphrase_env'])
            
            self.brokers[broker_name] = exchange_class(params)
        except Exception as e:
            print(f"Warning: Impossible d'initialiser {broker_name} - {str(e)}")
    
    def get_quote_asset(self, broker_name):
        """Retourne l'asset de cotation (USDC/USDT)"""
        return BROKER_CONFIG.get(broker_name, {}).get('quote_asset', 'USDT')

    # Ajout à la classe USDCArbitrage existante
    def set_broker(self, broker_name):
        """Permet de changer de broker dynamiquement"""
        if broker_name in BROKER_CONFIG:
            self.exchange = MultiBrokerArbitrage().brokers.get(broker_name)
            self.quote_asset = BROKER_CONFIG[broker_name]['quote_asset']
        else:
            raise ValueError(f"Broker {broker_name} non configuré")

    def get_available_brokers(self):
        """Liste des brokers configurés"""
        return list(BROKER_CONFIG.keys())
