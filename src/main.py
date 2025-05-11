from src.core.ai import TradingEngine
import pandas as pd


def main(mode='dev'):
    print(f"Initialisation du bot en mode {mode}...")
    engine = TradingEngine()
    print("Bot prêt")


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(
        sys.argv) > 1 and '--mode=' in sys.argv[1] else 'dev'
    main(mode.split('=')[1] if '=' in mode else mode)
