from flask import Flask, render_template, request
import joblib
from predict import predict_sentiment  # Assurez-vous que cela fonctionne avec votre structure actuelle
path = '/home/maa/Documents/GitHub/works/classification_tweets/data/'

# Charger le modèle et le vectorizer
model = joblib.load(path+'sentiment_analysis_model.pkl')
vectorizer = joblib.load(path+'vectorizer.pkl')  # Assurez-vous d'avoir sauvegardé le vectorizer lors de l'entraînement

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tweet = request.form['tweet']
        prediction = predict_sentiment(tweet, model, vectorizer)
        return render_template('index.html', prediction=prediction)
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
