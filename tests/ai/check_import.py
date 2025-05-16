import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

print("Tentative d'import de TechnicalCNN_LSTM...")
try:
    from ai.models.hybrid_engine import TechnicalCNN_LSTM
    print("Import réussi !")
except Exception as e:
    print("Import échoué :", e)
