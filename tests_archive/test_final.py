import tensorflow as tf
import numpy as np
import sys

print("=== TEST FINAL ===")
print("Python:", sys.executable)
print("TensorFlow:", tf.__version__)
print("GPU:", tf.config.list_physical_devices('GPU'))

# Test de performance
size = 5000
device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'

with tf.device(device):
    a = tf.random.normal((size, size))
    b = tf.random.normal((size, size))
    c = tf.matmul(a, b)
    print(f"\nRésultat: Matrice {size}x{size} sur {device} - OK")
