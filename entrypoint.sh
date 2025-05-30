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

# Créer un superutilisateur si demandé et s'il n'existe pas déjà
if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "Vérification du superutilisateur..."
  # Création d'un script Python temporaire pour éviter les problèmes d'indentation
  cat > /tmp/create_superuser.py << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$SUPERUSER_EMAIL').exists():
    User.objects.create_superuser('$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print('Superutilisateur créé avec succès.')
else:
    print('Le superutilisateur existe déjà.')
EOF
  # Exécution du script
  python manage.py shell < /tmp/create_superuser.py
  # Suppression du script temporaire
  rm /tmp/create_superuser.py
  echo "Vérification du superutilisateur terminée."
fi

# Démarrer l'application
if [ "$DEBUG" = "true" ]; then
  echo "Démarrage du serveur de développement..."
  exec python manage.py runserver 0.0.0.0:${PORT:-8001}
else
  echo "Démarrage du serveur de production avec gunicorn..."
  exec gunicorn alloriginal_backend.wsgi:application --bind 0.0.0.0:${PORT:-8001}
fi
