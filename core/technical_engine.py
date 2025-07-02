"""Technical Engine for Trading Bot"""
import logging
import numpy as np
from typing import List, Union

logger = logging.getLogger(__name__)


class TechnicalEngine:
    """Technical analysis engine for the trading bot"""
    
    def __init__(self):
        """Initialize the technical engine"""
        logger.info("Initializing Technical Engine")
    
    def compute(self, data: Union[List, np.ndarray]) -> dict:
        """
        Compute technical analysis signals from price data
        
        Args:
            data: Price data array or list
            
        Returns:
            dict: Technical analysis signals
        """
        try:
            if not data:
                return {"signal": "neutral", "strength": 0.0}
                
            # Simple moving average based signal
            prices = np.array(data)
            if len(prices) < 2:
                return {"signal": "neutral", "strength": 0.0}
            
            # Calculate simple trend signal
            recent_price = prices[-1]
            avg_price = np.mean(prices)
            
            if recent_price > avg_price * 1.02:
                signal = "buy"
                strength = min((recent_price / avg_price - 1) * 10, 1.0)
            elif recent_price < avg_price * 0.98:
                signal = "sell" 
                strength = min((1 - recent_price / avg_price) * 10, 1.0)
            else:
                signal = "neutral"
                strength = 0.0
                
            return {
                "signal": signal,
                "strength": strength,
                "price": recent_price,
                "avg_price": avg_price
            }
            
        except Exception as e:
            logger.error(f"Error in technical computation: {e}")
            return {"signal": "neutral", "strength": 0.0, "error": str(e)}