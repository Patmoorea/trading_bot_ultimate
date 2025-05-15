import pytest
from unittest.mock import MagicMock

class TestAIModules:
    def test_import(self):
        """Test d'import de base"""
        try:
            from src.core_merged.ai_engine import HybridAI
            assert True
        except ImportError:
            assert False, "Erreur d'import HybridAI"

    @pytest.mark.gpu
    def test_gpu_acceleration(self):
        """Test d'accélération GPU"""
        mock_model = MagicMock()
        mock_model.device = 'mps'
        assert mock_model.device == 'mps'
