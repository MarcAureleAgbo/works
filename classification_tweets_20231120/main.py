from data_preprocessing import prepare_data
from model_training import train_model, save
from model_evaluation import evaluate_model
from predict import predict_sentiment
from data_visualisation import plot_data
import pandas as pd

path = '/home/maa/Documents/GitHub/works/classification_tweets/data/'
filename = path+'training.1600000.processed.noemoticon.csv'
data = pd.read_csv(filename, encoding='ISO-8859-1')

# Charger et préparer les données
X_train, X_test, y_train, y_test, vectorizer = prepare_data(filename)

# Afficher la distribution des sentiments
plot_data(data,['target'])

# Entraîner le modèle
model = train_model(X_train, y_train)

# Sauvegarder le 'vectorizer'
save(vectorizer,path+'vectorizer.pkl')

# Évaluer le modèle
evaluate_model(model, X_test, y_test)

# Sauvegarder le modèle
save(model, path+'sentiment_analysis_model.pkl')

# Exemple de prédiction
tweet = "J'adore utiliser ChatGPT pour l'apprentissage !"
print(predict_sentiment(tweet, model, vectorizer))

