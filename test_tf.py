import tensorflow as tf
import time

print("=== Test TensorFlow ===")
print(f"Version: {tf.__version__}")
print(f"GPU: {tf.config.list_physical_devices('GPU')}")

size = 5000
device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'

with tf.device(device):
    start = time.time()
    a = tf.random.normal((size, size))
    b = tf.random.normal((size, size))
    c = tf.matmul(a, b)
    print(f"\nTemps calcul: {time.time()-start:.2f}s")
