#!/bin/bash

# Fonction pour attendre que PostgreSQL soit disponible
function postgres_ready(){
python << END
import sys
import psycopg2
import os

try:
    dbname = os.environ.get('DB_NAME', 'alloriginal_db')
    user = os.environ.get('DB_USER', 'alloriginal')
    password = os.environ.get('DB_PASSWORD', 'alloriginal_password')
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

# Attendre que PostgreSQL soit disponible
until postgres_ready; do
  echo "Attente de PostgreSQL..."
  sleep 2
done

echo "PostgreSQL est disponible, démarrage de l'application..."

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
if [ "$APPLY_MIGRATIONS" = "true" ]; then
  echo "Application des migrations..."
  python manage.py migrate
fi

# Démarrer l'application
if [ "$DEBUG" = "true" ]; then
  echo "Démarrage du serveur de développement..."
  exec python manage.py runserver 0.0.0.0:${PORT:-8001}
else
  echo "Démarrage du serveur de production avec gunicorn..."
  exec gunicorn alloriginal_backend.wsgi:application --bind 0.0.0.0:${PORT:-8001}
fi
