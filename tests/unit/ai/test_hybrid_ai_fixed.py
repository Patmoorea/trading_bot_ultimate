try:
    from src.core.ai.hybrid_ai_enhanced import HybridAIEnhanced
    from src.core.utils import optimize_for_m4
except ImportError as e:
    print(f"ImportError: {str(e)}")
    HybridAIEnhanced = None

import pytest

class TestHybridAIPerformance:
    @pytest.mark.skipif(HybridAIEnhanced is None, reason="Module non disponible")
    def test_initialization(self):
        ai = HybridAIEnhanced(config={"use_metal": True})
        assert ai.is_initialized == False

# Évolution : Ajout de l'affichage pour vérifier l'import effectif de HybridAIEnhanced
try:
    from src.core.ai.hybrid_ai_enhanced import HybridAIEnhanced as HybridAIEnhanced_V2
    from src.core.utils import optimize_for_m4 as optimize_for_m4_V2
    print("✅ HybridAIEnhanced_V2 imported:", HybridAIEnhanced_V2)
except ImportError as e:
    print(f"ImportError in V2 import block: {str(e)}")
    HybridAIEnhanced_V2 = None

# Évolution : test actif sur HybridAIEnhanced_V2 (sans skip)
class TestHybridAIPerformanceV2:
    def test_v2_initialization(self):
        if HybridAIEnhanced_V2 is None:
            pytest.fail("HybridAIEnhanced_V2 not imported")
        ai = HybridAIEnhanced_V2(config={"use_metal": True})
        assert hasattr(ai, "is_initialized")

def test_dummy_pass():
    assert 1 == 1

print("✅ DEBUG: HybridAIEnhanced_V2 is", HybridAIEnhanced_V2)

def test_import_direct_hybridai_v2():
    try:
        from src.core.ai.hybrid_ai_enhanced import HybridAIEnhanced as HybridAIEnhanced_V2_direct
        print("✅ Direct import HybridAIEnhanced_V2_direct:", HybridAIEnhanced_V2_direct)
    except ImportError as e:
        pytest.fail(f"ImportError direct: {str(e)}")
