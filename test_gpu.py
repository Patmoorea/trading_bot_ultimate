import tensorflow as tf

def test_gpu():
    gpus = tf.config.list_physical_devices('GPU')
    assert gpus, "Aucun GPU détecté - Vérifiez tensorflow-metal"
    print(f"[SUCCÈS] GPU détecté : {gpus[0]}")

if __name__ == "__main__":
    test_gpu()
