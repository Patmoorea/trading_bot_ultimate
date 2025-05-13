import logging
import time
import pandas as pd
from core.engine import TradingEngine
from core.technical_engine import TechnicalEngine

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def safe_analyze(tech_engine, data):
    """Version sécurisée de l'analyse technique"""
    try:
        return tech_engine.compute(data)
    except Exception as e:
        logger.error(f"Erreur d'analyse: {str(e)}")
        return {}

def main():
    try:
        # Initialisation
        engine = TradingEngine()
        tech_engine = TechnicalEngine()
        
        # Chargement des données
        logger.info("Chargement des données...")
        df = engine.load_data('data/historical/btc_usdt_1h_clean.csv')
        logger.info(f"Données chargées ({len(df)} points)")
        
        # Analyse technique
        while True:
            window = df.iloc[-100:]  # Dernières 100 bougies
            analysis = safe_analyze(tech_engine, window)
            
            # Affichage des résultats
            if analysis.get('momentum', {}).get('rsi') is not None:
                logger.info(f"RSI: {analysis['momentum']['rsi'].iloc[-1]:.2f}")
            
            if analysis.get('volatility', {}).get('bbands_BBU_20_2.0') is not None:
                logger.info("Bollinger Bands:")
                logger.info(f"  Upper: {analysis['volatility']['bbands_BBU_20_2.0'].iloc[-1]:.2f}")
                logger.info(f"  Middle: {analysis['volatility']['bbands_BBM_20_2.0'].iloc[-1]:.2f}")
                logger.info(f"  Lower: {analysis['volatility']['bbands_BBL_20_2.0'].iloc[-1]:.2f}")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Arrêt manuel demandé")
    except Exception as e:
        logger.error(f"Erreur critique: {str(e)}", exc_info=True)
    finally:
        logger.info("Bot arrêté")

if __name__ == '__main__':
    main()
