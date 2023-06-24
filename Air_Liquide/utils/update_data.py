
def update_data():
    import yfinance as yf
    import psycopg2
    # Établir une connexion à la base de données
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="AirLiquide",
        user="postgres"
    )
    # Créer un curseur pour exécuter les requêtes
    cur = conn.cursor()

    # Créer un objet Ticker pour AirLiquide
    ticker = yf.Ticker("AI.PA")

    # Obtenir les données historiques jusqu'à la dernière date disponible
    history = ticker.history(period="1d")

    # Récupérer la dernière valeur "Low" et la date correspondante
    last_low_value = history["Low"].iloc[-1]
    last_date = history.index[-1].date()

    # Afficher la date et la dernière valeur "Low" d'AirLiquide
    print("Date :", last_date)
    print("Dernière valeur Low d'AirLiquide :", last_low_value)

    # Exemple de mise à jour des valeurs dans la table
    nouvelle_date = last_date
    nouveau_low = last_low_value

    # Vérifier si le jour existe déjà dans la table
    cur.execute("SELECT date FROM raw_data WHERE date = %s", (nouvelle_date,))
    existing_date = cur.fetchone()

    if existing_date:
        # Le jour existe déjà dans la table
        print("Le jour existe déjà dans la base de données.")
    else:
        # Le jour n'existe pas dans la table, ajouter les données
        cur.execute("INSERT INTO raw_data (date, low) VALUES (%s, %s)", (nouvelle_date, nouveau_low))
        print("Données ajoutées avec succès.")

    # Valider la transaction
    conn.commit()

    # Fermer le curseur et la connexion à la base de données
    cur.close()
    conn.close()

    return "raw_data updated to "+str(nouvelle_date)


def update_pred(nouvelle_date,pred):
    import psycopg2
    # Établir une connexion à la base de données
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="AirLiquide",
        user="postgres"
    )
    # Créer un curseur pour exécuter les requêtes
    cur = conn.cursor()

    # Vérifier si le jour existe déjà dans la table
    cur.execute("SELECT date FROM ma_table WHERE date = %s", (nouvelle_date,))
    existing_date = cur.fetchone()

    if existing_date:
        # Le jour existe déjà dans la table
        print("Le jour existe déjà dans la base de données.")
    else:
        # Le jour n'existe pas dans la table, ajouter les données
        cur.execute("INSERT INTO predictions(date, valeur) VALUES (%s, %s)", (nouvelle_date, pred))
        print("Données ajoutées avec succès.")
    # Valider la transaction
    conn.commit()

    # Fermer le curseur et la connexion à la base de données
    cur.close()
    conn.close()

    return "predictions updated to "+str(nouvelle_date)



if __name__ == "__main__":
    #maj des données de la base
    update_data()
    #maj des valeurs prédites
#    update_pred()