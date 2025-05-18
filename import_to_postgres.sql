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
