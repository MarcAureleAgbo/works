import pandas as pd
import os
from utils.data_loading import load_data

# Définit le répertoire de travail actuel sur le dossier air_liquid/
os.chdir("/home/maa/Documents/GitHub/works/Air_Liquide/")

def preprocess_data(data):
    """
    Preprocess the data and return the preprocessed data
    """    
    # Rename columns
    data = data.rename(columns={'low': 'Price'})
    
    # count missing values 
    missing_values_count = data.isnull().sum()
    
    # Fill missing values
    if sum(missing_values_count.values) > 0:
        print('-> valeurs manquantes détectées')
        for col in data.columns:
            if data[col].dtype in ['float64','float32']:
                data[col].fillna(data[col].mean(), inplace=True)
                print('--> ', col, ': moyenne utilisée pour remplir les vides')
        else:
            data[col].fillna(data[col].mode()[0], inplace=True)
            print('--> ', col, ': mode utilisée pour remplir les vides')
    
    return data

if __name__ == "__main__":
    # Load the data
    data = load_data()
    
    # Preprocess the data
    preprocessed_data = preprocess_data(data)
    
    # show
    print(preprocessed_data.head(3))
    
    # Save the preprocessed data
    preprocessed_data.to_csv("./data/preprocessed_data.csv", index=False)
