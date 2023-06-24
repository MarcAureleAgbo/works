import pandas as pd

def load_data(file_path):
    """
    Load data from file_path and return the loaded data
    """
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def load_data():
    import psycopg2
    # Établir une connexion à la base de données
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="AirLiquide",
        user="postgres"
    )
    # Exécuter une requête pour récupérer les données de la table
    query = "SELECT * FROM raw_data order by date"
    df = pd.read_sql(query, conn)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.set_index('date')
    return df


if __name__ == "__main__":
    # Load the data
    data = load_data()
    
    # Print the first few rows of the data
    print(data.head())
