#!/bin/bash
# Script de migration de SQLite vers PostgreSQL pour AllOriginal

echo "Migration SQLite vers PostgreSQL"
echo "--------------------------------"

# Étape 1: Créer un script SQL à partir de la base SQLite
echo "Étape 1: Extraction du schéma SQLite..."
sqlite3 db.sqlite3 .schema > sqlite_schema.sql

# Étape 2: Modification manuelle pour compatibilité PostgreSQL
echo "Étape 2: Création du script d'adaptation pour PostgreSQL..."

cat > convert_sqlite_to_pg.sql << 'EOL'
-- Script pour adapter le schéma SQLite à PostgreSQL

-- Créer les tables nécessaires
-- Tables d'authentification
CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_staff BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_token (
    key VARCHAR(40) PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Tables de contenu
CREATE TABLE IF NOT EXISTS categories_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    icon_description VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS products_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(220) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    status VARCHAR(20) NOT NULL,
    is_featured BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    category_id INTEGER REFERENCES categories_category(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products_productimage (
    id SERIAL PRIMARY KEY,
    image VARCHAR(100) NOT NULL,
    is_primary BOOLEAN NOT NULL,
    alt_text VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    product_id INTEGER REFERENCES products_product(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products_productspecification (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    value VARCHAR(255) NOT NULL,
    is_highlighted BOOLEAN NOT NULL,
    display_order INTEGER NOT NULL,
    product_id INTEGER REFERENCES products_product(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS accounts_userprofile (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(10),
    country VARCHAR(100),
    photo VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Ajustement des séquences
SELECT setval('auth_user_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM auth_user), false);
SELECT setval('categories_category_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM categories_category), false);
SELECT setval('products_product_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM products_product), false);
SELECT setval('products_productimage_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM products_productimage), false);
SELECT setval('products_productspecification_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM products_productspecification), false);
SELECT setval('accounts_userprofile_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM accounts_userprofile), false);
EOL

# Étape 3: Extraire les données SQLite et les insérer dans les fichiers CSV
echo "Étape 3: Extraction des données depuis SQLite..."

# Utilisateurs
sqlite3 -header -csv db.sqlite3 "SELECT id, password, last_login, is_superuser, email, first_name, last_name, is_active, is_staff, date_joined FROM accounts_user" > users.csv

# Catégories
sqlite3 -header -csv db.sqlite3 "SELECT id, name, slug, description, icon, icon_description, is_active, created_at, updated_at FROM categories_category" > categories.csv

# Produits
sqlite3 -header -csv db.sqlite3 "SELECT id, name, slug, description, category_id, brand, model, price, original_price, status, is_featured, is_active, created_at, updated_at FROM products_product" > products.csv

# Images produits
sqlite3 -header -csv db.sqlite3 "SELECT id, product_id, image, is_primary, alt_text, created_at FROM products_productimage" > product_images.csv

# Spécifications produits
sqlite3 -header -csv db.sqlite3 "SELECT id, product_id, name, value, is_highlighted, display_order FROM products_productspecification" > product_specs.csv

# Profils utilisateurs
sqlite3 -header -csv db.sqlite3 "SELECT id, user_id, phone_number, address, city, postal_code, country, photo, created_at, updated_at FROM accounts_userprofile" > user_profiles.csv

# Étape 4: Créer un script pour importer les données dans PostgreSQL
echo "Étape 4: Préparation de l'importation vers PostgreSQL..."

cat > import_to_postgres.sql << 'EOL'
-- Importation des données depuis les fichiers CSV vers PostgreSQL

-- Utilisateurs
COPY auth_user(id, password, last_login, is_superuser, email, first_name, last_name, is_active, is_staff, date_joined)
FROM '/home/markupsafe/Documents/AllOriginalBackend/users.csv' DELIMITER ',' CSV HEADER;

-- Catégories
COPY categories_category(id, name, slug, description, icon, icon_description, is_active, created_at, updated_at)
FROM '/home/markupsafe/Documents/AllOriginalBackend/categories.csv' DELIMITER ',' CSV HEADER;

-- Produits
COPY products_product(id, name, slug, description, category_id, brand, model, price, original_price, status, is_featured, is_active, created_at, updated_at)
FROM '/home/markupsafe/Documents/AllOriginalBackend/products.csv' DELIMITER ',' CSV HEADER;

-- Images produits
COPY products_productimage(id, product_id, image, is_primary, alt_text, created_at)
FROM '/home/markupsafe/Documents/AllOriginalBackend/product_images.csv' DELIMITER ',' CSV HEADER;

-- Spécifications produits
COPY products_productspecification(id, product_id, name, value, is_highlighted, display_order)
FROM '/home/markupsafe/Documents/AllOriginalBackend/product_specs.csv' DELIMITER ',' CSV HEADER;

-- Profils utilisateurs
COPY accounts_userprofile(id, user_id, phone_number, address, city, postal_code, country, photo, created_at, updated_at)
FROM '/home/markupsafe/Documents/AllOriginalBackend/user_profiles.csv' DELIMITER ',' CSV HEADER;
EOL

echo "Étape 5: Exécution des scripts SQL PostgreSQL..."

# Exécuter le script de création des tables dans PostgreSQL
PGPASSWORD=alloriginal_password psql -h localhost -U alloriginal -d alloriginal_db -f convert_sqlite_to_pg.sql

# Exécuter le script d'importation des données
PGPASSWORD=alloriginal_password psql -h localhost -U alloriginal -d alloriginal_db -f import_to_postgres.sql

echo "Migration terminée!"
echo "Vérifiez les éventuelles erreurs dans les messages ci-dessus."
echo "Pensez à lancer les migrations Django pour créer les tables manquantes."
