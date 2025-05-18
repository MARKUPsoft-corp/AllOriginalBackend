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
