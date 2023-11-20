from data_preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer

def predict_sentiment(tweet, model, vectorizer):
    # Prétraitement du tweet
    cleaned_tweet = preprocess_text(tweet)

    # Vectorisation
    vectorized_tweet = vectorizer.transform([cleaned_tweet])

    # Prédiction
    prediction = model.predict(vectorized_tweet)

    sentiment = 'Positif' if prediction == 4 else 'Négatif'
    return sentiment


