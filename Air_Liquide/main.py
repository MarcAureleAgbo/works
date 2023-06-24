import os, argparse
import numpy as np
import pandas as pd
from preprocessing.preprocessing import preprocess_data
from utils.data_loading import load_data
from models.model import build_model
from utils.model_evaluation import evaluate_model_rnn
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import TimeSeriesSplit
import matplotlib.pyplot as plt
from joblib import dump

parser = argparse.ArgumentParser(description='---')
parser.add_argument('--test', action='store_true', help='Scission des données en train/test ou entrainement sur toutes les données train')
args = parser.parse_args()


if __name__ == "__main__":
    PATH = '/home/maa/Documents/GitHub/works/Air_Liquide'
    os.chdir(PATH)
    
    if args.test: #données scindées train/test
        target_column = 'Price'
        test_size = 100
        print('-> taille des données de test: ',test_size,'\n')    
        # Load the data
        data = load_data()
        
        # Preprocess the data
        preprocessed_data = preprocess_data(data)
        #preprocessed_data.reset_index(drop=True, inplace=True)
        
        # Split the data into training and test sets
        train_data = preprocessed_data[:-test_size]
        test_data = preprocessed_data[-test_size:]
        
        # Mise à l'échelle des données
        scaler = MinMaxScaler()
        scaler.fit(train_data) #on fait le fit uniquement sur le train parce que le test ne peut en aucun cas participer aux travaux ici
        
        scaled_train = scaler.transform(train_data)
        scaled_test = scaler.transform(test_data)
        print('-> mise à échelle effectuée!','\n')
        
        # Générateur de séries temporelles (obtenir 12 jours en arrière et prédire le jour suivant)
        length = 30 #12
        generator = TimeseriesGenerator(scaled_train, scaled_train, length=length, batch_size=1)
    
        # A quoi ressemble le premier batch ?
        X,y = generator[0]

        # Build the model
        n_features = 1
        n_epochs = 100
        monitor, patience ='val_loss', 10
        batch_size = 1
        
        model = build_model((length, n_features))
        
        # EarlyStopping qui controle val_loss
        early_stop = EarlyStopping(monitor=monitor,patience=patience)
        
        # Générateur de validation
        validation_generator = TimeseriesGenerator(scaled_test,scaled_test, length=length, batch_size=batch_size)
        
        # Train the model
        print('-> création du modèle avec les paramètres ci-après:')
        print(' early_stop: monitor:',monitor,', patience:',patience)
        print('n_features: ',n_features)
        print('epochs: ',n_epochs,'\n')
        
        model.fit(generator, epochs=n_epochs, 
                validation_data=validation_generator,
                callbacks=[early_stop])
        
        # Evaluate the model on the test data
        losses = pd.DataFrame(model.history.history)
        losses.plot()
        plt.show()
        
        mse, test_data_2 = evaluate_model_rnn(model, test_data, scaled_train, length, n_features, scaler)
        
        # Print the MSE
        print("-> MSE:", mse)
        
        # Save the trained model
        model.save("./models/trained_model.h5")
        
        # Save the test data
        dump(length, './data/length.joblib')
        dump(n_features, './data/n_features.joblib')
        dump(scaled_train, './data/scaled_train.joblib')    
        dump(test_data[['Price']], './data/test_data.joblib')    
        dump(scaler, './data/scaler.joblib')

    else: # toutes les données pour le modèle final (avec validation croisée)

        target_column = 'Price'
        print('-> Ici, toutes les données servent pour lentrainement\n')    
        # Load the data
        data = load_data()
        
        # Preprocess the data
        train_data = preprocess_data(data)
        
        # Mise à l'échelle des données
        scaler = MinMaxScaler()
        scaler.fit(train_data) 
        scaled_train = scaler.transform(train_data)
        
        print('-> mise à échelle effectuée!','\n')
        
        # Générateur de séries temporelles (obtenir 12 jours en arrière et prédire le jour suivant)
        length = 30 #12
        generator = TimeseriesGenerator(scaled_train, scaled_train, length=length, batch_size=1)      
        
        # Build the model
        n_features = 1
        n_epochs = 100
        monitor, patience ='val_loss', 10
        batch_size = 1
        
        model = build_model((length, n_features))
        
        # EarlyStopping qui controle val_loss
        early_stop = EarlyStopping(monitor=monitor,patience=patience)
        
        # générateur de validation croisée
        n_folds = 5
        tscv = TimeSeriesSplit(n_splits=n_folds)
        scores = []        
        
        # boucle sur les splits de la cross-validation
        for train_index, val_index in tscv.split(train_data):
            # Création des générateurs pour l'ensemble d'entraînement et de validation
            train_gen = TimeseriesGenerator(train_data.values[train_index], train_data.values[train_index], length=length, batch_size=batch_size)
            val_gen = TimeseriesGenerator(train_data.values[val_index], train_data.values[val_index], length=length, batch_size=batch_size)
    
            # Entraînement du modèle sur l'ensemble d'entraînement
            model.fit(train_gen, epochs=10, callbacks=[early_stop]) #, verbose=0)
    
            # Évaluation du modèle sur l'ensemble de validation
            score = model.evaluate(val_gen, verbose=0)
            scores.append(score)
            
        # Évaluation globale de la performance de la cross-validation
        print("Moyenne des scores de la cross-validation : %.2f%%" % (np.mean(scores)*100))

        
        # Entrainement sur l'ensemble des données d'entrainement
        print('-> création du modèle avec les paramètres ci-après:')
        print(' early_stop: monitor:',monitor,', patience:',patience)
        print('n_features: ',n_features)
        print('epochs: ',n_epochs,'\n')
        
        model.fit(generator, epochs=n_epochs,
                callbacks=[early_stop]) #, verbose=0)
        
        # Evaluate the model on the test data
        losses = pd.DataFrame(model.history.history)
        losses.plot()
        plt.show()
        
        #mse, test_data_2 = evaluate_model_rnn(model, test_data, scaled_train, length, n_features, scaler)

        # nombre de valeurs à prédire
        periods = 7 
        # les dates associées en partant du 1er jour qui suit le dernier jour des train
        pred_index = pd.date_range(start=(pd.to_datetime(max(train_data.index)) + pd.Timedelta(days=1)).strftime('%Y-%m-%d'), periods=periods, freq='D')
        
        first_eval_batch = scaled_train[-length:]
        current_batch = first_eval_batch.reshape((1, length, n_features))
        
        valeurs_predites = []
        
        for i in range(periods):
            # prediction avec 1 periode d'avance
            current_pred = model.predict(current_batch)[0]
        
            # stocker la prédiction
            valeurs_predites.append(current_pred) 
        
            # mise à jour du batch pour inclure maintenant la prédiction et supprimer la première valeur
            current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)        
        
        valeurs_predites = scaler.inverse_transform(valeurs_predites)
        predictions = pd.DataFrame(data=valeurs_predites, index=pred_index, columns=['predictions'])
        print(predictions.head(3))
        
        
        # Save the trained model
        model.save("./models/full_trained_model.h5")
        
        # Save the test data
        dump(length, './data/length.joblib')
        dump(n_features, './data/n_features.joblib')
        dump(scaled_train, './data/full_scaled_train.joblib')        
        dump(scaler, './data/scaler_full.joblib')
        
        # tracer les données avec les prédictions sur la même courbe
        ax = train_data.plot()
        predictions.plot(ax=ax)
        plt.show()                
        
        # tracer les données avec les prédictions sur la même courbe (ZOOMER sur 10 jours avant et periods jours apres)
        ax = train_data.plot()
        predictions.plot(ax=ax)
        debut_zoom = (pd.to_datetime(max(train_data.index)) - pd.Timedelta(days=7))
        fin_zoom =  (pd.to_datetime(max(train_data.index)) + pd.Timedelta(days=periods))
        plt.xlim(debut_zoom, fin_zoom)
        plt.show()
        
