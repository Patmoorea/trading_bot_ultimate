import pytest
import os
import sys
from datetime import datetime

root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root_dir)

CURRENT_TIME = "2025-05-19 00:19:29"
CURRENT_USER = "Patmoorea"

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    yield

@pytest.fixture
def mock_datetime(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime.strptime(CURRENT_TIME, "%Y-%m-%d %H:%M:%S")
    monkeypatch.setattr("datetime.datetime", MockDateTime)
    return MockDateTime

@pytest.fixture
def current_user():
    return CURRENT_USER
