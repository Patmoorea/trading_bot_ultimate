#!/bin/bash
source /Users/patricejourdan/venv_trading/bin/activate
cd /Users/patricejourdan/trading_bot_ultimate
PYTHONPATH=$(pwd) python -m pytest tests/unit/ -v --cov=src.core $@
