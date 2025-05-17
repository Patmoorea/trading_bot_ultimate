class AdvancedMultiTimeframeAnalyzer:
    INDICATORS = {
        'trend': ['ichimoku', 'supertrend', 'vwma'],
        'momentum': ['rsi', 'stoch_rsi', 'macd'],
        'volatility': ['atr', 'bb_width', 'keltner'],
        'volume': ['obv', 'vwap', 'accumulation'],
        'orderflow': ['bid_ask_ratio', 'liquidity_wave', 'smart_money_index']
    }
    
    @staticmethod
    def detect_regime(data):
        """Détection adaptive des régimes de marché"""
        regimes = {
            0: 'High Volatility Bull',
            1: 'Low Volatility Bull',
            2: 'High Volatility Bear',
            3: 'Low Volatility Bear',
            4: 'Sideways'
        }
        return regimes[model.predict(data[-100:])]
