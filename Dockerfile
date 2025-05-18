FROM python:3.10-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8001

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application
COPY . .

# Exposer le port
EXPOSE 8001

# Script d'entrée pour attendre PostgreSQL et démarrer l'application
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Commande d'entrée
ENTRYPOINT ["/entrypoint.sh"]
