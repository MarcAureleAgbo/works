from utils import preprocess_data, plot_results, visualize_metrics
from models import run_model, predict

def main():
    # Prétraitez les données
    data = preprocess_data()
    
    # Entraînez et évaluez le modèle
    run_model()
    
    # Prédisez les valeurs futures
    predictions = predict(model, data)
    
    # Visualisez les résultats
    plot_results()
    visualize_metrics()
    
if __name__ == '__main__':
    main()
