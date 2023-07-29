import psycopg2
import pandas as pd
from datetime import datetime, timedelta


def update_data():
    """
    S'assurer que le fichier AI.PA.csv est à jour. A cette étape, le remplacer manuellement. TODO: Trouver une solution de le remplacer automatiquement
    """
    # Établir une connexion à la base de données
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="AirLiquide",
        user="postgres"
    )
    # Créer un curseur pour exécuter les requêtes
    cur = conn.cursor()

    # dernière date dans en bdd
    cur.execute("SELECT max(date) FROM raw_data")
    derniere_date_bdd = cur.fetchone()[0]

    # dernière date renseignée en ligne
    df = pd.read_csv('/home/maa/Documents/GitHub/works/Air_Liquide/data/AI.PA.csv', parse_dates=['Date'])
    df = df.sort_values('Date', ascending=False).reset_index(drop=True)[['Date','Low']]
    derniere_date_a_jour = df.Date[0].date()

    # Dates à mettre à jour
    dates_maj = []
    date_origine = derniere_date_bdd
    while derniere_date_bdd <= derniere_date_a_jour:
        if derniere_date_bdd != date_origine:
            dates_maj.append(derniere_date_bdd.strftime('%Y-%m-%d'))
        derniere_date_bdd += timedelta(days=1)

    print("Démarrage de la mise à jour:\n")

    if dates_maj != []:
        
        for d in dates_maj:
            print(str(d))
            low = df[df.Date == d]['Low'].iloc[0]
            cur.execute("INSERT INTO raw_data (date, low) VALUES (%s, %s)", (d, low))
        print("Done")
    else:
        print("Aucune date manquante!")
    # Valider la transaction
    conn.commit()
    
    # Fermer le curseur et la connexion à la base de données
    cur.close()
    conn.close()

    return "raw_data updated to " + str(derniere_date_a_jour)

   

def update_pred(nouvelle_date,pred):
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
    cur.execute("SELECT date FROM predictions WHERE date = %s", (nouvelle_date,))
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
    
    # Mise à jour des données de la base
    update_data()
    
    # maj des valeurs prédites
    # update_pred()
