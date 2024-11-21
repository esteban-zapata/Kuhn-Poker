import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models

def create_model(input_shape):
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=input_shape))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid')) #two actions pass (p) and bet (b)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def encode_history(history, max_lenght=2):
    encoding = {'p': 0, 'b': 1}
    encoded = np.array([encoding[char] for char in history], dtype=np.float32)
    padded = np.pad(encoded, (0, max_lenght - len(encoded)), 'constant', constant_values=-1)
    return padded
