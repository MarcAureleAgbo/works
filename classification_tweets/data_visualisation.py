
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(data, columns):
    """
    Affiche des graphiques adaptés au type de données des colonnes spécifiées.

    :param data: DataFrame Pandas contenant les données.
    :param columns: Nom de la colonne ou liste de noms de colonnes.
    """
    if isinstance(columns, str):
        columns = [columns]

    for column in columns:
        if pd.api.types.is_numeric_dtype(data[column]):
            # Visualisation pour les données numériques
            plt.figure()
            sns.histplot(data[column], kde=True)
            plt.title(f'Distribution de {column}')
            plt.xlabel(column)
            plt.ylabel('Fréquence')
        elif pd.api.types.is_categorical_dtype(data[column]) or pd.api.types.is_object_dtype(data[column]):
            # Visualisation pour les données qualitatives
            plt.figure()
            sns.countplot(x=column, data=data)
            plt.title(f'Comptage pour {column}')
            plt.xlabel(column)
            plt.ylabel('Nombre')
        plt.show()
    return 

