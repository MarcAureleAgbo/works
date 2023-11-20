from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib


def train_model(X_train, y_train):
    # Création du modèle
    model = LogisticRegression()

    # Entraînement du modèle
    model.fit(X_train, y_train)

    return model

def save(model, filename):
    joblib.dump(model, filename)

