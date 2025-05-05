import tensorflow as tf

def configure_apple_silicon():
    """Configure TensorFlow for Apple Silicon GPU acceleration"""
    try:
        # Vérifier si Metal est disponible
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"GPU Apple Silicon détecté: {gpus}")
            # Configuration des optimisations spécifiques
            tf.config.optimizer.set_jit(True)  # Activation XLA
            tf.config.threading.set_inter_op_parallelism_threads(8)
            tf.config.threading.set_intra_op_parallelism_threads(8)
            return True
        return False
    except Exception as e:
        print(f"Warning: Configuration GPU échouée - {str(e)}")
        return False

# Exécuter automatiquement à l'import
GPU_ACTIVATED = configure_apple_silicon()
