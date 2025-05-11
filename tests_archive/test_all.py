import numpy as np
import tensorflow as tf
import talib
from modules.arbitrage_engine import ArbitrageEngine

def test_environment():
    print(f"NumPy: {np.__version__}")
    print(f"TensorFlow GPU: {tf.test.is_gpu_available()}")
    print(f"TA-Lib: {talib.SMA([1,2,3], timeperiod=2)[-1] == 2.5}")
    
    engine = ArbitrageEngine()
    print(f"Whitelist: {engine.config.get('whitelist', [])}")

if __name__ == "__main__":
    test_environment()
