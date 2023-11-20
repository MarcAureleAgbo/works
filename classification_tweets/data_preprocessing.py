import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
path = '/home/maa/Documents/GitHub/works/classification_tweets/data/'

# Télécharger les stopwords de NLTK
nltk.download('stopwords')
nltk.download('wordnet')

def load_data(filename):
#    data = pd.read_csv(filename)
    data = pd.read_csv(filename, encoding='ISO-8859-1')
    return data

def preprocess_text(text):
    # Supprimer les mentions, hashtags et URLs
    text = re.sub(r'@\w+|#\w+|http\S+', '', text)
    
    # Convertir en minuscules
    text = text.lower()
    
    # Supprimer la ponctuation et les chiffres
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenisation
    words = text.split()
    
    # Supprimer les stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    return ' '.join(words)

def prepare_data(filename):
    data = load_data(filename)
    data['cleaned_text'] = data['text'].apply(preprocess_text)
    
    # Séparer les données
    X_train, X_test, y_train, y_test = train_test_split(
        data['cleaned_text'], data['target'], test_size=0.2, random_state=42)
    
    # Vectorisation
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)
    
    return X_train, X_test, y_train, y_test, vectorizer