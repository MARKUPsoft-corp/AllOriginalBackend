-- Importation des données depuis les fichiers CSV vers PostgreSQL avec \copy
-- Cette commande fonctionne pour tous les utilisateurs

-- Utilisateurs
\copy auth_user(id, password, last_login, is_superuser, email, first_name, last_name, is_active, is_staff, date_joined) FROM '/home/markupsafe/Documents/AllOriginalBackend/users.csv' WITH CSV HEADER DELIMITER ',';

-- Catégories
\copy categories_category(id, name, slug, description, icon, icon_description, is_active, created_at, updated_at) FROM '/home/markupsafe/Documents/AllOriginalBackend/categories.csv' WITH CSV HEADER DELIMITER ',';

-- Produits
\copy products_product(id, name, slug, description, category_id, brand, model, price, original_price, status, is_featured, is_active, created_at, updated_at) FROM '/home/markupsafe/Documents/AllOriginalBackend/products.csv' WITH CSV HEADER DELIMITER ',';

-- Images produits
\copy products_productimage(id, product_id, image, is_primary, alt_text, created_at) FROM '/home/markupsafe/Documents/AllOriginalBackend/product_images.csv' WITH CSV HEADER DELIMITER ',';

-- Spécifications produits
\copy products_productspecification(id, product_id, name, value, is_highlighted, display_order) FROM '/home/markupsafe/Documents/AllOriginalBackend/product_specs.csv' WITH CSV HEADER DELIMITER ',';

-- Profils utilisateurs
\copy accounts_userprofile(id, user_id, phone_number, address, city, postal_code, country, photo, created_at, updated_at) FROM '/home/markupsafe/Documents/AllOriginalBackend/user_profiles.csv' WITH CSV HEADER DELIMITER ',';
