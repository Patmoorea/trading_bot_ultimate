from src.core_merged.ai.hybrid_ai_enhanced import HybridAIEnhanced
import pytest
import asyncio

class TestHybridAIEnhanced:
    @pytest.fixture
    def ai_config(self):
        return {
            'model_path': 'models/hybrid_v2.mdl',
            'enable_metal': True
        }

    @pytest.mark.asyncio
    async def test_init(self, ai_config):
        ai = HybridAIEnhanced(**ai_config)
        assert ai.is_initialized is False
        await ai.initialize()
        assert ai.is_initialized is True
    
    # ... (conservez ici vos autres tests existants) ...
