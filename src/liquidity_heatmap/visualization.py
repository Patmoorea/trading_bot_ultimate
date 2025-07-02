"""Liquidity Heatmap Visualization Module - Enhanced with error handling"""
import logging
import numpy as np
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

def generate_heatmap(orderbook: Union[Dict, None], levels: int = 20) -> Dict:
    """
    Generate liquidity heatmap from orderbook data with robust error handling
    
    Args:
        orderbook: Orderbook data with bids and asks
        levels: Number of price levels to analyze
        
    Returns:
        dict: Heatmap data structure
    """
    try:
        if not orderbook or not isinstance(orderbook, dict):
            logger.warning("Invalid orderbook data provided")
            return _create_empty_heatmap()
        
        bids = orderbook.get('bids', [])
        asks = orderbook.get('asks', [])
        
        if not bids or not asks:
            logger.warning("Missing bids or asks in orderbook")
            return _create_empty_heatmap()
        
        # Convert to numpy arrays with error handling
        try:
            bids_array = np.array(bids[:levels])
            asks_array = np.array(asks[:levels])
            
            if bids_array.size == 0 or asks_array.size == 0:
                return _create_empty_heatmap()
            
            # Ensure we have at least 2 columns (price, volume)
            if bids_array.ndim < 2 or bids_array.shape[1] < 2:
                return _create_empty_heatmap()
            if asks_array.ndim < 2 or asks_array.shape[1] < 2:
                return _create_empty_heatmap()
            
        except (ValueError, IndexError) as e:
            logger.error(f"Error converting orderbook to arrays: {e}")
            return _create_empty_heatmap()
        
        # Calculate heatmap intensities
        try:
            # Normalize volumes to 0-1 range
            bid_volumes = bids_array[:, 1].astype(float)
            ask_volumes = asks_array[:, 1].astype(float)
            
            max_bid_vol = np.max(bid_volumes) if len(bid_volumes) > 0 else 1
            max_ask_vol = np.max(ask_volumes) if len(ask_volumes) > 0 else 1
            
            bid_heat = (bid_volumes / max_bid_vol) if max_bid_vol > 0 else np.zeros_like(bid_volumes)
            ask_heat = (ask_volumes / max_ask_vol) if max_ask_vol > 0 else np.zeros_like(ask_volumes)
            
        except Exception as e:
            logger.error(f"Error calculating heat intensities: {e}")
            return _create_empty_heatmap()
        
        # Create heatmap structure
        heatmap = {
            'bid_levels': [
                {
                    'price': float(bids_array[i, 0]),
                    'volume': float(bids_array[i, 1]),
                    'heat_intensity': float(bid_heat[i])
                }
                for i in range(len(bids_array))
            ],
            'ask_levels': [
                {
                    'price': float(asks_array[i, 0]),
                    'volume': float(asks_array[i, 1]),
                    'heat_intensity': float(ask_heat[i])
                }
                for i in range(len(asks_array))
            ],
            'best_bid': float(bids_array[0, 0]) if len(bids_array) > 0 else 0,
            'best_ask': float(asks_array[0, 0]) if len(asks_array) > 0 else 0,
            'spread': float(asks_array[0, 0] - bids_array[0, 0]) if len(bids_array) > 0 and len(asks_array) > 0 else 0,
            'total_bid_volume': float(np.sum(bid_volumes)),
            'total_ask_volume': float(np.sum(ask_volumes)),
            'levels_analyzed': min(levels, len(bids), len(asks)),
            'status': 'success'
        }
        
        logger.info(f"Generated heatmap with {len(heatmap['bid_levels'])} bid and {len(heatmap['ask_levels'])} ask levels")
        return heatmap
        
    except Exception as e:
        logger.error(f"Error generating heatmap: {e}")
        return _create_empty_heatmap()


def _create_empty_heatmap() -> Dict:
    """Create empty heatmap structure for fallback"""
    return {
        'bid_levels': [],
        'ask_levels': [],
        'best_bid': 0,
        'best_ask': 0,
        'spread': 0,
        'total_bid_volume': 0,
        'total_ask_volume': 0,
        'levels_analyzed': 0,
        'status': 'error',
        'message': 'Unable to generate heatmap from provided data'
    }


def visualize_heatmap_text(heatmap: Dict) -> str:
    """
    Create a simple text visualization of the heatmap
    
    Args:
        heatmap: Heatmap data structure
        
    Returns:
        str: Text representation
    """
    try:
        if heatmap.get('status') == 'error':
            return f"Heatmap Error: {heatmap.get('message', 'Unknown error')}"
        
        lines = [
            "=== Liquidity Heatmap ===",
            f"Best Bid: {heatmap['best_bid']:.6f}",
            f"Best Ask: {heatmap['best_ask']:.6f}",
            f"Spread: {heatmap['spread']:.6f}",
            f"Total Bid Volume: {heatmap['total_bid_volume']:.2f}",
            f"Total Ask Volume: {heatmap['total_ask_volume']:.2f}",
            f"Levels Analyzed: {heatmap['levels_analyzed']}"
        ]
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"Error creating visualization: {e}"


# Test function
def test_heatmap_generation():
    """Test the heatmap generation with sample data"""
    try:
        sample_orderbook = {
            'bids': [
                [50000.0, 1.5],
                [49950.0, 2.0],
                [49900.0, 3.2]
            ],
            'asks': [
                [50100.0, 1.2],
                [50150.0, 1.8],
                [50200.0, 2.5]
            ]
        }
        
        heatmap = generate_heatmap(sample_orderbook)
        print("Heatmap test successful!")
        print(visualize_heatmap_text(heatmap))
        return True
        
    except Exception as e:
        print(f"Heatmap test failed: {e}")
        return False


if __name__ == "__main__":
    test_heatmap_generation()
