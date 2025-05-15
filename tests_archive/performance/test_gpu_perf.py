import tensorflow as tf
from src.core_merged.gpu_config import configure_gpu

def test_gpu():
    print("=== Test TensorFlow ===")
    print(f"Version: {tf.__version__}")
    
    try:
        gpu_ok = configure_gpu()
        print(f"GPU configuré: {gpu_ok}")
        
        # Test de performance
        device = '/GPU:0' if gpu_ok else '/CPU:0'
        with tf.device(device):
            size = 10000
            a = tf.random.normal((size, size))
            b = tf.random.normal((size, size))
            print(f"Calcul matrice {size}x{size} sur {device}...")
            tf.matmul(a, b)
            print("Test réussi")
        return gpu_ok
    except Exception as e:
        print(f"Échec du test: {str(e)}")
        return False

if __name__ == "__main__":
    test_gpu()
