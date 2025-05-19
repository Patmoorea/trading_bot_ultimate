import pytest
import os
import sys
from datetime import datetime
import numpy as np
from typing import Optional

# Ensure src is in path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Set test environment variables
os.environ.update({
    'TELEGRAM_BOT_TOKEN': 'test_token',
    'TELEGRAM_CHAT_ID': 'test_chat_id',
    'EXCHANGE_API_KEY': 'test_key',
    'EXCHANGE_API_SECRET': 'test_secret',
    'IS_TEST': 'true',
    'MODEL_PATH': 'models/',
    'PERFORMANCE_LOG_PATH': 'logs/performance/'
})

class BaseTest:
    @pytest.fixture(autouse=True)
    def init_test(self):
        """Initialize test environment"""
        self.timestamp = "2025-05-19 00:47:05"  # Updated timestamp
        self.user = "Patmoorea"
        from config import Config
        self.config = Config()
        yield

    def get_test_data(self, size: int = 100) -> np.ndarray:
        """Generate test data"""
        return np.random.random(size)

    @staticmethod
    def assert_timestamp_format(timestamp_str: str) -> bool:
        """Validate timestamp format"""
        try:
            datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
