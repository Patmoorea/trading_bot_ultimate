"""Risk Manager for Trading Bot"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RiskManager:
    """Risk management system for the trading bot"""
    
    def __init__(self):
        """Initialize the risk manager"""
        self.max_drawdown = 0.05  # 5% max drawdown
        self.max_position_size = 0.1  # 10% max position size
        logger.info("Initializing Risk Manager")
    
    def evaluate_risk(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate risk for a given trading signal
        
        Args:
            signal: Trading signal from technical analysis
            
        Returns:
            dict: Risk assessment and recommendations
        """
        try:
            if not signal or not isinstance(signal, dict):
                return {
                    "risk_level": "high",
                    "position_size": 0.0,
                    "recommendation": "no_trade",
                    "reason": "Invalid signal"
                }
            
            signal_strength = signal.get("strength", 0.0)
            signal_type = signal.get("signal", "neutral")
            
            # Calculate risk level based on signal strength
            if signal_strength > 0.8:
                risk_level = "low"
                position_size = self.max_position_size * 0.8
            elif signal_strength > 0.5:
                risk_level = "medium"
                position_size = self.max_position_size * 0.5
            elif signal_strength > 0.2:
                risk_level = "medium_high"
                position_size = self.max_position_size * 0.3
            else:
                risk_level = "high"
                position_size = 0.0
            
            # Determine recommendation
            if signal_type == "neutral" or position_size == 0.0:
                recommendation = "no_trade"
            elif signal_type in ["buy", "sell"]:
                recommendation = "trade_allowed"
            else:
                recommendation = "monitor"
            
            return {
                "risk_level": risk_level,
                "position_size": position_size,
                "recommendation": recommendation,
                "signal_strength": signal_strength,
                "max_drawdown": self.max_drawdown
            }
            
        except Exception as e:
            logger.error(f"Error in risk evaluation: {e}")
            return {
                "risk_level": "high",
                "position_size": 0.0,
                "recommendation": "no_trade",
                "reason": f"Error: {str(e)}"
            }