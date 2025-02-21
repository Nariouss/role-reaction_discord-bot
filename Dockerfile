FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000 pour le health check
EXPOSE 8000

# Lancer le bot Discord et Flask
CMD ["python", "bot.py"]
