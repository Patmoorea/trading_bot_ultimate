import tensorflow as tf
from src.core_merged.base_model import create_base_model

model = create_base_model()
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='binary_crossentropy')

print("=== Test Réussi ===")
print("Architecture du modèle:")
model.summary()
