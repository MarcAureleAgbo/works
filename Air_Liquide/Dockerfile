# Définir l'image de base (ici je choisis tensorflow pour simplifier l'environnement et de toute façon il comporte deja python 3.8)
FROM tensorflow/tensorflow:latest

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY requirements.txt .
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# port
EXPOSE 8080

# Définir la commande de démarrage
CMD ["python3", "/app/main.py"]
