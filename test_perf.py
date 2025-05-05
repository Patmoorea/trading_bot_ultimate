import tensorflow as tf
import time

def benchmark():
    size = 10000
    device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'
    
    with tf.device(device):
        start = time.time()
        a = tf.random.normal((size, size))
        b = tf.random.normal((size, size))
        c = tf.matmul(a, b)
        return time.time() - start

print(f"Temps calcul: {benchmark():.2f}s")
