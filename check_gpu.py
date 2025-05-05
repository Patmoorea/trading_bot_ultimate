import tensorflow as tf
print("=== Vérification Conda ===")
print(f"TensorFlow: {tf.__version__}")
print(f"GPU détectés: {tf.config.list_physical_devices('GPU')}")
