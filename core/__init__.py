import tensorflow as tf

# Initialisation automatique du statut GPU
try:
    GPU_AVAILABLE = len(tf.config.list_physical_devices('GPU')) > 0
except:
    GPU_AVAILABLE = False

def check_gpu_status():
    """Retourne le statut actuel du GPU"""
    return GPU_AVAILABLE
