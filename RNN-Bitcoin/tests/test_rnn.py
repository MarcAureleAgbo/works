import pytest
from rnn import build_model

def test_build_model():
    # Test if build_model returns a valid Keras model
    model = build_model(input_shape=(50, 1))
    assert isinstance(model, keras.Sequential)
    assert len(model.layers) == 3
    assert isinstance(model.layers[0], keras.layers.LSTM)
    assert isinstance(model.layers[1], keras.layers.Dropout)
    assert isinstance(model.layers[2], keras.layers.Dense)
    assert model.input_shape == (None, 50, 1)
    assert model.output_shape == (None, 1)

