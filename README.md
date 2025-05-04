# AllOriginal Backend API

Backend Django pour le site e-commerce AllOriginal, fournissant une API REST pour le frontend Nuxt.js.

## Installation

1. Cloner le dépôt
2. Installer les dépendances: `pip install -r requirements.txt`
3. Appliquer les migrations: `python manage.py migrate`
4. Créer un superutilisateur: `python manage.py createsuperuser`
5. Lancer le serveur de développement: `python manage.py runserver`

## Architecture

Le backend est structuré en plusieurs applications Django:

- **accounts**: Gestion des utilisateurs et de l'authentification
- **categories**: Gestion des catégories de produits
- **products**: Gestion des produits, images et spécifications

## Points d'API

### Catégories
- `GET /api/categories/` - Liste des catégories
- `GET /api/categories/{slug}/` - Détail d'une catégorie
- `GET /api/categories/{slug}/products/` - Produits d'une catégorie

### Produits
- `GET /api/products/` - Liste des produits
- `GET /api/products/{slug}/` - Détail d'un produit
- `GET /api/products/featured/` - Produits mis en avant
- `GET /api/products/search/?q={query}` - Recherche de produits

### Authentification
- `POST /api/accounts/register/` - Inscription
- `POST /api/accounts/login/` - Connexion
- `POST /api/accounts/logout/` - Déconnexion
- `GET /api/accounts/me/` - Utilisateur actuel
- `GET/PUT /api/accounts/profile/` - Profil utilisateur

## Documentation de l'API

Une documentation interactive de l'API est disponible à l'URL `/api/docs/`.

## Migration vers PostgreSQL

Pour utiliser PostgreSQL au lieu de SQLite:

1. Installer psycopg2: `pip install psycopg2-binary`
2. Modifier le fichier `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alloriginal',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Créer une base de données PostgreSQL: `createdb alloriginal`
4. Appliquer les migrations: `python manage.py migrate`
