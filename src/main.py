import os
import sys
import logging
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.technical_engine import TechnicalEngine
from core.risk_manager import RiskManager

# Chargement de la configuration
load_dotenv()
config = {
    "NEWS": {
        "enabled": True,
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "")
    }
}

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    init_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("⚡ Initialisation du Trading Bot M4")
        engine = TechnicalEngine()
        risk_mgr = RiskManager()
        
        # Simulation de données
        test_data = [1.5, 2.3, 3.1, 4.0]
        
        logger.info("Analyse des données...")
        signal = engine.compute(test_data)
        risk_assessment = risk_mgr.evaluate_risk(signal)
        
        logger.info(f"Signal: {signal}")
        logger.info(f"Évaluation du risque: {risk_assessment}")
        
        # Test des composants AI avec gestion d'erreurs
        try:
            logger.info("Test des composants IA...")
            bot = TradingBot()
            logger.info("✓ TradingBot initialisé avec succès")
        except Exception as ai_error:
            logger.warning(f"Erreur composants IA: {ai_error}")
            logger.info("Bot fonctionne en mode dégradé sans IA")
        
    except KeyboardInterrupt:
        logger.info("Arrêt manuel demandé")
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
    finally:
        logger.info("Bot arrêté")


# ========== IMPORT OPTIMISÉ AVEC GESTION D'ERREURS ==========
def safe_import_ai_modules():
    """Import des modules IA avec fallback gracieux"""
    components = {}
    
    # News analyzer avec fallback
    try:
        from src.news_processor.core import CachedNewsSentimentAnalyzer
        components['news_analyzer'] = CachedNewsSentimentAnalyzer
        print("✓ CachedNewsSentimentAnalyzer chargé")
    except ImportError:
        try:
            from src.news_processor.core import NewsSentimentAnalyzer
            components['news_analyzer'] = NewsSentimentAnalyzer
            print("ℹ NewsSentimentAnalyzer chargé (fallback)")
        except ImportError as e:
            print(f"⚠ News analyzer non disponible: {e}")
            components['news_analyzer'] = None
    
    # Regime detector avec fallback
    try:
        from src.regime_detection.hmm_kmeans import MarketRegimeDetector
        components['regime_detector'] = MarketRegimeDetector
        print("✓ MarketRegimeDetector chargé")
    except ImportError as e:
        print(f"⚠ Regime detector non disponible: {e}")
        components['regime_detector'] = None
    
    # Quantum SVM avec fallback
    try:
        from src.quantum_ml.qsvm import QuantumSVM
        components['qsvm'] = QuantumSVM
        print("✓ QuantumSVM chargé")
    except ImportError as e:
        print(f"⚠ QuantumSVM non disponible: {e}")
        components['qsvm'] = None
    
    return components


class TradingBot:
    def __init__(self):
        """Initialize TradingBot with error handling for AI components"""
        self.components = safe_import_ai_modules()
        
        # Initialize components with fallback
        try:
            if self.components['news_analyzer']:
                self.news_analyzer = self.components['news_analyzer']()
            else:
                self.news_analyzer = None
                
            if self.components['regime_detector']:
                self.regime_detector = self.components['regime_detector']()
            else:
                self.regime_detector = None
                
            if self.components['qsvm']:
                self.qsvm = self.components['qsvm']()
            else:
                self.qsvm = None
                
        except Exception as e:
            logging.warning(f"Erreur initialisation composants IA: {e}")
            self.news_analyzer = None
            self.regime_detector = None
            self.qsvm = None

    def update_heatmap(self):
        """Update liquidity heatmap with error handling"""
        try:
            # Import with fallback
            from src.liquidity_heatmap.visualization import generate_heatmap
            # This would normally fetch from exchange
            # orderbook = self.exchange.fetch_order_book("BTC/USDT")
            # self.current_heatmap = generate_heatmap(orderbook)
            print("Heatmap update simulation (exchange not connected)")
        except ImportError as e:
            logging.warning(f"Heatmap not available: {e}")
        except Exception as e:
            logging.error(f"Erreur update heatmap: {e}")


if __name__ == "__main__":
    main()
