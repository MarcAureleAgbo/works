import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

def build_model(input_shape):
    """
    Build the RNN model and return the model
    """
    model = Sequential()
    model.add(LSTM(units=128, activation='relu', input_shape=input_shape))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mse', metrics=['mse','mae','mape'])
    return model

if __name__ == "__main__":
    # Set the input shape
    input_shape = (None, 1)
    
    # Build the model
    model = build_model(input_shape)
    
    # Print the model summary
    model.summary()
