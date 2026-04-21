import mysql.connector
from config import DB_CONFIG

con = mysql.connector.connect(**DB_CONFIG)
cur = con.cursor(dictionary=True)

# Check all product colors
print("=== ALL PRODUCT COLORS ===")
cur.execute("SELECT * FROM product_colors ORDER BY product_id, id")
colors = cur.fetchall()
for color in colors:
    print(f"ID: {color['id']}, Product ID: {color['product_id']}, Color: {color['color']}, Image: {color['color_image']}")

print("\n=== PRODUCTS WITH COLOR COUNT ===")
cur.execute("""
    SELECT p.id, p.name, COUNT(pc.id) as color_count
    FROM products p
    LEFT JOIN product_colors pc ON p.id = pc.product_id
    GROUP BY p.id, p.name
    ORDER BY p.id
""")
products = cur.fetchall()
for prod in products:
    print(f"Product ID: {prod['id']}, Name: {prod['name']}, Colors: {prod['color_count']}")

cur.close()
con.close()
