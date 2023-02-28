import pytest
from preprocess import load_data, preprocess_data

def test_load_data():
    # Test if load_data returns expected data shape
    data = load_data("data/bitcoin_data.csv")
    assert data.shape == (365, 1)

def test_preprocess_data():
    # Test if preprocess_data returns expected data shape and type
    data = load_data("data/bitcoin_data.csv")
    X_train, y_train, X_test, y_test = preprocess_data(data, seq_len=50)
    assert isinstance(X_train, np.ndarray)
    assert isinstance(y_train, np.ndarray)
    assert isinstance(X_test, np.ndarray)
    assert isinstance(y_test, np.ndarray)
    assert X_train.shape == (255, 50, 1)
    assert y_train.shape == (255, 1)
    assert X_test.shape == (60, 50, 1)
    assert y_test.shape == (60, 1)

