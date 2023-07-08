import psycopg2
import yfinance as yf
from datetime import date, timedelta

# Établir une connexion à la base de données
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="AirLiquide",
    user="postgres"
)
# Créer un curseur pour exécuter les requêtes
cur = conn.cursor()

def update_data(date):
    # Créer un objet Ticker pour AirLiquide
    ticker = yf.Ticker("AI.PA")

    # Obtenir les données historiques jusqu'à la date spécifiée
    history = ticker.history(start=date, end=date)

    if history.empty:
        print("Aucune donnée disponible pour la date spécifiée.")
        return

    # Récupérer la valeur "Low" et la date correspondante
    low_value = history["Low"].iloc[0]
    date = history.index[0].date()

    # Afficher la date et la valeur "Low" d'AirLiquide
    print("Date :", date)
    print("Valeur Low d'AirLiquide :", low_value)

    # Vérifier si la date existe déjà dans la table
    cur.execute("SELECT date FROM raw_data WHERE date = %s", (date,))
    existing_date = cur.fetchone()

    if existing_date:
        # La date existe déjà dans la table
        print("La date existe déjà dans la base de données.")
    else:
        # La date n'existe pas dans la table, ajouter les données
        cur.execute("INSERT INTO raw_data (date, low) VALUES (%s, %s)", (date, low_value))
        print("Données ajoutées avec succès.")

    # Valider la transaction
        conn.commit()

    return "raw_data updated to " + str(date)

def update_pred(nouvelle_date,pred):
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
    return "predictions updated to "+str(nouvelle_date)



if __name__ == "__main__":
    
    # dates à mettre à jour
    cur.execute("SELECT max(date) FROM raw_data")
    derniere_date = cur.fetchone()[0]
    aujourd_hui = date.today()
    liste_dates = []
    delta = timedelta(days=1)
    current_date = derniere_date
    while current_date <= aujourd_hui:
        liste_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += delta

    print("liste des dates à MAJ: ",liste_dates)

    
    
    
    # Mise à jour des données de la base
#    for d in liste_dates:
#        update_data(date=d)
    # maj des valeurs prédites
    # update_pred()







    # Fermer le curseur et la connexion à la base de données
    cur.close()
    conn.close()