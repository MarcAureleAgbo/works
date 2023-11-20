from sklearn.metrics import classification_report

def evaluate_model(model, X_test, y_test):
    # Prédiction sur l'ensemble de test
    y_pred = model.predict(X_test)

    # Évaluation du modèle
    report = classification_report(y_test, y_pred)
    print(report)
