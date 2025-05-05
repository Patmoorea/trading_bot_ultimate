from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_base_model(input_shape=(100, 5)):
    model = Sequential([
        LSTM(64, input_shape=input_shape, return_sequences=True),
        LSTM(32),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    return model
