import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from joblib import load

# def evaluate_model(model, X_test, y_test):
#     """
#     Evaluate the trained model on the test data and return the MSE
#     """
#     y_pred = model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     return mse


def evaluate_model_rnn(model, test_data, scaled_train, length, n_features, scaler):
    test_predictions = []

    first_eval_batch = scaled_train[-length:]
    current_batch = first_eval_batch.reshape((1, length, n_features))

    for i in range(len(test_data)):
        
        # obtenir la prédiction avec 1 timestamp d'avance ([0] pour ne saisir que le nombre au lieu de [array])
        current_pred = model.predict(current_batch)[0]
        
        # stocker la prédiction
        test_predictions.append(current_pred) 
        
        # mise à jour du batch pour inclure maintenant la prédiction et supprimer la première valeur
        current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

    true_predictions = scaler.inverse_transform(test_predictions)
    
    print('shape de true_predictions: ',true_predictions.shape)
    print('shape de test_data: ', test_data.shape)
    
    test_data['Predictions'] = true_predictions
    
    # Tracer les prédictions en fonction des valeurs réelles du test
    test_data.plot(figsize=(12,8))
    plt.show()

    mse = np.sqrt(mean_squared_error(test_data['Price'],test_data['Predictions']))
    
    return (mse, test_data)


if __name__ == "__main__":
    # Load the test data
    test_data = load("./data/test_data.joblib")
    scaled_train = load("./data/scaled_train.joblib")
    length = load('./data/length.joblib')
    n_features = load('./data/n_features.joblib')
    scaler = load('./data/scaler.joblib')
    
    # show
    
    
    # Load the trained model
    model = tf.keras.models.load_model("./models/trained_model.h5")
    
    # Evaluate the model on the test data
    mse, test_data_2 = evaluate_model_rnn(model, test_data, scaled_train, length, n_features, scaler)
    
    # Print the MSE
    print("MSE:", mse)
