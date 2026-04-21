CREATE DATABASE trendify_db;
USE trendify_db;

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
INSERT INTO admin(username, password)
VALUES ('admin', 'admin123');

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    gender VARCHAR(20),
    age INT,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
INSERT INTO categories(name) VALUES ('trending');
INSERT INTO categories(name) VALUES ('occasion');
INSERT INTO categories(name) VALUES ('mostselling');

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    description TEXT,
    quality VARCHAR(100),
    quantity INT DEFAULT 0,
    size VARCHAR(50),
    image VARCHAR(255),

    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id) REFERENCES categories(id)
    ON DELETE SET NULL
);

CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,

    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY (product_id) REFERENCES products(id)
    ON DELETE CASCADE
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount INT NOT NULL,
    order_status VARCHAR(50) DEFAULT 'Pending',
    payment_method VARCHAR(50) DEFAULT 'COD',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,

    FOREIGN KEY (order_id) REFERENCES orders(id)
    ON DELETE CASCADE,

    FOREIGN KEY (product_id) REFERENCES products(id)
    ON DELETE CASCADE
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'Pending',
    transaction_id VARCHAR(100),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
    ON DELETE CASCADE
);

CREATE TABLE return_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    reason TEXT,
    return_status VARCHAR(50) DEFAULT 'Requested',
    return_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
    ON DELETE CASCADE,

    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO admins (username, password) VALUES 
('admin', 'admin123');

SHOW TABLES;
SELECT * FROM categories;
SELECT * FROM admin;
SHOW COLUMNS FROM users;
DESCRIBE users;
SHOW DATABASES;
USE trendify_db;
DESC users;
SELECT * FROM users;
SHOW COLUMNS FROM products;
SELECT * FROM categories;
SELECT * FROM products;
USE trendify_db;
SELECT * FROM products;
SELECT * FROM products WHERE category_id = 1;
SELECT COUNT(*) FROM products;
USE trendify_db;
INSERT INTO products(name, price, description, quality, quantity, size, image, category_id)
VALUES
('Denim Jacket', 550, 'Stylish casual denim wear', 'Premium Denim', 20, 'S,M,L,XL', 'denim_jecket.jpeg', 1),

('Leather Watch', 450, 'Elegant minimalist analog watch', 'Premium Leather Strap', 30, 'One Size', 'brown_watch.jpg', 1),

('Printed Shirt', 400, 'Light weight printed short sleeve shirt', 'Cotton Fabric', 25, 'S,M,L,XL', 'styalish.jpg', 1),

('Streetwear Hoodie Set', 800, 'Comfort meets fashion hoodie set', 'Winter Wear', 20, 'S,M,L,XL,XXL', 'comfort.jpg', 1),

('Low-Top Sneakers', 2199, 'Classic white & grey street sneakers', 'Rubber Sole + Premium Leather', 15, '7,8,9,10,12', 'sneakers.jpg', 1),

('Half-Zip Sweatshirt', 550, 'Premium half-zip sweatshirt modern design', 'Cotton Blend', 18, 'S,M,L,XL,XXL', 'sweatshirt.jpg', 1),

('Couple Coordinated Outfit', 2500, 'Elegant coordinated couple outfit', 'Premium Fabric', 10, 'S,M,L,XL,XXL', 'couple_outfits.jpg', 1),

('High-Waist Cargo Pants', 650, 'High-waist beige cargo pants', 'Cotton Cargo Fabric', 22, 'M,L,XL', 'cargo_pents.jpg', 1);
SELECT id, name, image, category_id FROM products;

CREATE TABLE IF NOT EXISTS product_colors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    color VARCHAR(50) NOT NULL,
    color_image VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Denim Jacket'), 'black', 'denim_jecket.jpeg'),
((SELECT id FROM products WHERE name='Denim Jacket'), 'wine', 'denim_wine.jpg'),
((SELECT id FROM products WHERE name='Denim Jacket'), 'blue', 'denim_blue.jpg');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Leather Watch'), 'brown', 'brown_watch.jpg'),
((SELECT id FROM products WHERE name='Leather Watch'), 'navy', 'neavy_blue_watch.png'),
((SELECT id FROM products WHERE name='Leather Watch'), 'tan', 'tan.png'),
((SELECT id FROM products WHERE name='Leather Watch'), 'green', 'forest_green_watch.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Printed Shirt'), 'white', 'styalish.jpg'),
((SELECT id FROM products WHERE name='Printed Shirt'), 'maroon', 'maroon_shirt.png'),
((SELECT id FROM products WHERE name='Printed Shirt'), 'olive', 'olive_green_shirt.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Streetwear Hoodie Set'), 'white', 'comfort.jpg'),
((SELECT id FROM products WHERE name='Streetwear Hoodie Set'), 'brown', 'brown_hoodie.png'),
((SELECT id FROM products WHERE name='Streetwear Hoodie Set'), 'black', 'black_hoodie.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Half-Zip Sweatshirt'), 'green', 'sweatshirt.jpg'),
((SELECT id FROM products WHERE name='Half-Zip Sweatshirt'), 'maroon', 'maroon_sweat.png'),
((SELECT id FROM products WHERE name='Half-Zip Sweatshirt'), 'brown', 'brown_sweat.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Couple Coordinated Outfit'), 'navy', 'couple_outfits.jpg'),
((SELECT id FROM products WHERE name='Couple Coordinated Outfit'), 'green', 'bottle_green.png'),
((SELECT id FROM products WHERE name='Couple Coordinated Outfit'), 'brown', 'brown_couple-outfit.png'),
((SELECT id FROM products WHERE name='Couple Coordinated Outfit'), 'gray', 'gray_couple-outfit.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='High-Waist Cargo Pants'), 'cream', 'cargo_pents.jpg'),
((SELECT id FROM products WHERE name='High-Waist Cargo Pants'), 'blue', 'blue_cargo.png'),
((SELECT id FROM products WHERE name='High-Waist Cargo Pants'), 'pink', 'pink.png');

SELECT * FROM product_colors;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM product_colors;

USE trendify_db;


SELECT product_id, COUNT(*) 
FROM product_colors
GROUP BY product_id;

USE trendify_db;
INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Printed Shirt', 400, 'Light weight printed shirt', 'Cotton Blend', 25, 'S,M,L,XL', 'styalish.jpg', 1);

SELECT id, name FROM products ORDER BY id DESC;

SELECT id, name FROM products WHERE name='Printed Shirt';

SELECT * FROM product_colors WHERE product_id IN (3,9);
DELETE FROM products WHERE id = 9;
SELECT * FROM product_colors WHERE product_id = 3;
SELECT * FROM product_colors WHERE product_id = 9;
SELECT * FROM products;

INSERT INTO product_colors (product_id, color, color_image)
VALUES
(3, 'white', 'styalish.jpg'),
(3, 'maroon', 'maroon_shirt.png'),
(3, 'olive', 'olive_green_shirt.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
(4, 'white', 'comfort.jpg'),
(4, 'brown', 'brown_hoodie.png'),
(4, 'black', 'black_hoodie.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
(6, 'green', 'sweatshirt.jpg'),
(6, 'maroon', 'maroon_sweat.png'),
(6, 'brown', 'brown_sweat.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
(7, 'navy', 'couple_outfits.jpg'),
(7, 'green', 'bottle_green.png'),
(7, 'brown', 'brown_couple-outfit.png'),
(7, 'gray', 'gray_couple-outfit.png');

SELECT * FROM product_colors WHERE product_id IN (3,4,6,7);
USE trendify_db;
SHOW TABLES;
SELECT * FROM cart;
SELECT * FROM admin;
SELECT * FROM users;
SELECT * FROM products WHERE category_id = 2;
SELECT * FROM categories;
SELECT * FROM products;
SELECT * FROM product_colors;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM products 
WHERE name IN (
  'Diwali - Kurta Set'
);
SHOW TABLE STATUS LIKE 'products';
ALTER TABLE products AUTO_INCREMENT = 9;

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Diwali - Kurta Set', 1150,
'Stylish embroidered kurta set perfect for festive occasions with elegant detailing and a comfortable fit.',
'Premium Fabric', 20, 'S,M,L,XL', 'kurta set.png', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Diwali - Kurti Pants', 850,
'Beautiful ethnic kurti with palazzo pants, designed for festive wear with a classy traditional look.',
'Cotton Fabric', 25, 'S,M,L,XL', 'yello.png', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Diwali - Traditional Kurta Pajama', 900,
'Traditional kurta pajama with a modern festive style, ideal for celebrations and special functions.',
'Cotton Fabric', 20, 'S,M,L,XL', 'white.png', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Karva Chauth - Mirror Work Kurti', 900,
'Trendy festive kurti with mirror work design, perfect for traditional events and party wear.',
'Mirror Work Fabric', 18, 'S,M,L,XL,XXL', 'p1.png', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Cocktail Party Saree', 2499,
'Designer saree perfect for cocktail parties and special occasions, giving a classy and elegant look.',
'Premium Saree Fabric', 15, 'Free Size', 'sarii.jpg', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Karva Chauth - Saree', 3000,
'Traditional saree designed for festive celebrations, giving a graceful and elegant appearance.',
'Premium Saree Fabric', 12, 'Free Size', 'red.png', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Mehandi / Haldi Sherwani', 3000,
'Stylish embroidered sherwani designed for wedding functions like Mehandi and Haldi ceremonies.',
'Premium Sherwani Fabric', 10, 'S,M,L,XL,XXL', 'bgreen.png', 2);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Couple Coordinated Outfit', 5000,
'Elegant coordinated couple outfit with a modern festive style, perfect for parties and functions.',
'Premium Fabric', 10, 'S,M,L,XL,XXL', 'cocktail.png', 2);

DELETE FROM products WHERE name IN (
  'Couple Coordinated Outfit'
);

INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
VALUES ('Cocktail Party Outfit', 5000,
'Elegant party outfit with a modern festive style, perfect for parties and special functions.',
'Premium Fabric', 10, 'S,M,L,XL,XXL', 'cocktail.png', 2);

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Diwali - Kurta Set'), 'blue', 'blue_kurta.png'),
((SELECT id FROM products WHERE name='Diwali - Kurta Set'), 'pink', 'kurta set.png'),
((SELECT id FROM products WHERE name='Diwali - Kurta Set'), 'green', 'green_kurta.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Diwali - Kurti Pants'), 'yellow', 'yello.png'),
((SELECT id FROM products WHERE name='Diwali - Kurti Pants'), 'purple', 'purple.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Diwali - Traditional Kurta Pajama'), 'white', 'white.png'),
((SELECT id FROM products WHERE name='Diwali - Traditional Kurta Pajama'), 'blue', 'blue.png');

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Karva Chauth - Mirror Work Kurti'), 'purple', 'p1.png'),
((SELECT id FROM products WHERE name='Karva Chauth - Mirror Work Kurti'), 'green', 'green.png'),
((SELECT id FROM products WHERE name='Karva Chauth - Mirror Work Kurti'), 'pink', 'pink1.png');

SELECT id, name FROM products WHERE name='Mehandi or Haldi Sherwani';

INSERT INTO product_colors (product_id, color, color_image)
VALUES
((SELECT id FROM products WHERE name='Mehandi / Haldi Sherwani'), 'green', 'bgreen.png'),
((SELECT id FROM products WHERE name='Mehandi / Haldi Sherwani'), 'yellow', 'y.png'),
((SELECT id FROM products WHERE name='Mehandi / Haldi Sherwani'), 'pink', 'pink2.png');

SELECT * FROM categories;

SELECT id, name, category_id FROM products WHERE category_id = 3;
SELECT id, name, image FROM products WHERE category_id = 3;

SELECT name, image FROM products;
ALTER TABLE products ADD COLUMN is_most_selling TINYINT(1) DEFAULT 0;

SELECT * FROM products
WHERE name IN (
    'Leather Watch',
    'Streetwear Hoodie Set',
    'Low-Top Sneakers',
    'Cocktail Party Saree',
    'Half-Zip Sweatshirt',
    'Couple Coordinated Outfit',
    'Karva Chauth - Mirror Work Kurti'
);
SELECT id, name FROM products;


INSERT INTO products(name, price, description, quality, quantity, size, image, category_id)
VALUES
('Couple Coordinated Outfit', 2500, 'Elegant coordinated couple outfit', 'Premium Fabric', 10, 'S,M,L,XL,XXL', 'couple_outfits.jpg', 1);

ALTER TABLE products 
ADD COLUMN most_selling_image VARCHAR(255);

UPDATE products 
SET most_selling_image = 'forest_green_watch.png'
WHERE id = 2;

UPDATE products 
SET most_selling_image = 'brown_hoodie.png'
WHERE id = 4;

UPDATE products 
SET most_selling_image = 'brown_sweat.png'
WHERE id = 6;

UPDATE products 
SET most_selling_image = 'pink2.png'
WHERE id = 15;

UPDATE products 
SET most_selling_image = 'p1.png'
WHERE id = 12;

SELECT id, name, is_most_selling FROM products;

CREATE TABLE most_selling_products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    color VARCHAR(50),
    image VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO most_selling_products (product_id, color, image) VALUES
(2, 'green', 'forest_green_watch.png'),
(19, 'brown', 'brown_hoodie.png'),
(6, 'brown', 'brown_sweat.png'),
(15, 'pink', 'pink2.png'),
(12, 'purple', 'p1.png');

SELECT id, name FROM products;

INSERT INTO most_selling_products (product_id, color, image) VALUES
(2, 'green', 'forest_green_watch.png'),
(4, 'brown', 'brown_hoodie.png'),
(5, 'white', 'sneakers.jpg'),
(6, 'brown', 'brown_sweat.png'),
(15, 'pink', 'pink2.png'),
(12, 'purple', 'p1.png');

INSERT INTO most_selling_products (product_id, color, image) VALUES
(13, 'black', 'sarii.jpg');

ALTER TABLE most_selling_products 
ADD COLUMN size VARCHAR(50);

UPDATE most_selling_products 
SET size = 'S, M, L, XL, XXL'
WHERE product_id = 4;

UPDATE most_selling_products 
SET size = '8, 9, 10, 11'
WHERE product_id = 5; 

UPDATE most_selling_products 
SET size = 'S, M, L, XL, XXL'
WHERE product_id = 6;

UPDATE most_selling_products 
SET size = 'S, M, L, XL, XXL'
WHERE product_id = 15;

UPDATE most_selling_products 
SET size = 'S, M, L, XL, XXL'
WHERE product_id = 12; 

UPDATE most_selling_products 
SET size = 'FREE SIZE'
WHERE product_id = 13;

SELECT product_id, size FROM most_selling_products;

SELECT * FROM cart;

ALTER TABLE cart ADD color_id INT;
SELECT * FROM users;
USE trendify_db;

RENAME TABLE admin TO admins;
RENAME TABLE admins TO admin;

select * from products;

CREATE TABLE IF NOT EXISTS product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

select * from product_images;

INSERT INTO product_images (product_id, image_path, display_order) 
VALUES (1, 'front_denim_clack.png', 0);

INSERT INTO product_images (product_id, image_path, display_order) 
VALUES (1, 'back_denim_black.png', 1);

INSERT INTO product_images (product_id, image_path, display_order) 
VALUES (1, 'back_wine_denim.png', 2);

-- Wine denim - Front view (same product, different color)
INSERT INTO product_images (product_id, image_path, display_order) 
VALUES (1, 'front_wine_denim.png', 3);

INSERT INTO product_images (product_id, image_path, display_order) 
VALUES (1, 'front_denim_blue.png', 4);

INSERT INTO product_images (product_id, image_path, display_order) 
VALUES (1, 'back_denim_blue.png', 5);

-- Delete old incorrect entries
DELETE FROM product_images WHERE product_id = 1;

-- Insert correct ones
INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(1, 'front_denim_black.png', 0),
(1, 'back_denim_black.png', 1),
(1, 'back_wine_denim.png', 2),
(1, 'front_wine_denim.png', 3),
(1, 'blue_front_denim.png', 4);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(3, 'printed_front.png', 0),
(3, 'printed_side.png', 1),
(3, 'printed_back.png', 2),
(3, 'maroon_printed_front.png', 3),
(3, 'maroon_printed_side.png', 4),
(3, 'maroon_printed_back.png', 5),
(3, 'olive_green_shirt_front.png', 6),
(3, 'olive_green_shirt_back.png', 7),
(3, 'olive_green_shirt_side.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(18, 'couple_outfit_blue_front.png', 0),
(18, 'couple_outfit_blue_back.png', 1),
(18, 'couple_outfit_blue_side.png', 2),
(18, 'couple_outfit_brown_front.png', 3),
(18, 'couple_outfit_brown_back.png', 4),
(18, 'couple_outfit_brown_side.png', 5),
(18, 'couple_outfit_gray_front.png', 6),
(18, 'couple_outfit_gray_back.png', 7),
(18, 'couple_outfit_gray_side.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(19, 't-shirt_front.png', 0),
(19, 't-shirt_side.png', 1),
(19, 't-shirt_back.png', 2);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(8, 'cargo_front.png', 0),
(8, 'cargo_1_front.png', 1),
(8, 'cargo_side.png', 2),
(8, 'cargo_front_blue.png', 3),
(8, 'cargo_1_blue.png', 4),
(8, 'cargo_blue_side.png', 5),
(8, 'pink_cargo_front.png', 6),
(8, 'pink_cargo_1.png', 7),
(8, 'pink_cargo_side.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(6, 'brown_sweat_front.png', 0),
(6, 'brown_sweat_side.png', 1),
(6, 'brown_sweat_back.png', 2),
(6, 'maroon_sweat_front.png', 3),
(6, 'maroon_sweat_side.png', 4),
(6, 'maroon_sweat_back.png', 5),
(6, 'green_sweat_front.png', 6),
(6, 'green_sweat_side.png', 7),
(6, 'green_sweat_back.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(4, 'gray_hoodie_front.png', 0),
(4, 'gray_hoodie_side.png', 1),
(4, 'gray_hoodie_back.png', 2),
(4, 'brown_hoodie_front.png', 3),
(4, 'brown_hoodie_side.png', 4),
(4, 'brown_hoodie_back.png', 5),
(4, 'bllack_hoodie_front.png', 6),
(4, 'black_hoodie_side.png', 7),
(4, 'black_hoodie_back.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(9, 'red_kurta_front.png', 0),
(9, 'red_kurta_back.png', 1),
(9, 'red_kurta_side.png', 2),
(9, 'blue_kurta_front.png', 3),
(9, 'blue_kurta_back.png', 4),
(9, 'blue_kurta_side.png', 5),
(9, 'green_kurta_front.png', 6),
(9, 'green_kurta_back.png', 7),
(9, 'green_kurta_side.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(10, 'ykurti_front.png', 0),
(10, 'ykurti_back.png', 1),
(10, 'ykurti_side.png', 2),
(10, 'pkurti_front.png', 3),
(10, 'pkurti_back.png', 4),
(10, 'pkurti_side.png', 5);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(11, 'white_front.png', 0),
(11, 'white_back.png', 1),
(11, 'white_side.png', 2),
(11, 'blue_front.png', 3),
(11, 'blue_back.png', 4),
(11, 'blue_side.png', 5);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(12, 'p1_front.png', 0),
(12, 'p1_back.png', 1),
(12, 'p1_side.png', 2),
(12, 'g1_front.png', 3),
(12, 'g1_back.png', 4),
(12, 'p_front.png', 5),
(12, 'p_back.png', 6),
(12, 'p_side.png', 7);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(13, 's_front.png', 0),
(13, 's_back.png', 1),
(13, 's_side.png', 2);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(14, 'r_front.png', 0),
(14, 'r_back.png', 1),
(14, 'r_side.png', 2);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(15, 'gk_front.png', 0),
(15, 'gk_side.png', 1),
(15, 'gk_back.png', 2),
(15, 'yk_front.png', 3),
(15, 'yk_side.png', 4),
(15, 'yk_back.png', 5),
(15, 'pk_front.png', 6),
(15, 'pk_side.png', 7),
(15, 'pk_back.png', 8);

INSERT INTO product_images (product_id, image_path, display_order) VALUES 
(17, 'ck_front.png', 0),
(17, 'ck_side.png', 1),
(17, 'ck_back.png', 2);

CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

UPDATE products SET name = 'Leather Jacket' WHERE id = 1;

UPDATE products SET description = "Men's Biker Leather Jacket" WHERE id = 1;
UPDATE products SET quality = 'Genuine Leather, YKK Zippers, Quilted Lining' WHERE id = 1;

UPDATE products SET name = 'Floral Printed Shirt' WHERE id = 3;

SELECT id, name, category_id FROM products WHERE name LIKE '%Couple%';
UPDATE products SET image = 't-shirt_front.png' WHERE id = 19;

SELECT * FROM product_images WHERE product_id = 19;
DELETE FROM product_images WHERE product_id = 19 AND image_path = 't-shirt.jpg';
UPDATE products SET price = 999 WHERE id = 19;

UPDATE products SET name = 'Women’s Ethnic Kurti Palazzo Set' WHERE id = 10;
select * from products;
use trendify_db;
UPDATE products SET name = 'Festive Mirror Embellished Velvet Kurti' WHERE id = 12;
UPDATE products SET name = 'Luxury Black Party Wear Saree' WHERE id = 13;
CREATE TABLE IF NOT EXISTS return_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    reason VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE return_requests ADD COLUMN refund_status VARCHAR(50) DEFAULT 'Pending';
ALTER TABLE return_requests ADD COLUMN admin_note VARCHAR(500) DEFAULT NULL;

