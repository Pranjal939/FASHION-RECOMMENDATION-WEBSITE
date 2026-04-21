import mysql.connector
from config import DB_CONFIG

con = mysql.connector.connect(**DB_CONFIG)
cur = con.cursor()

print("=== REMOVING DUPLICATE COLORS ===")

# Remove duplicate colors for Product ID 3 (Printed Shirt)
print("Removing duplicates for Product ID 3 (Printed Shirt)...")
cur.execute("DELETE FROM product_colors WHERE id IN (24, 25, 26)")
print(f"Deleted {cur.rowcount} duplicate colors")

# Remove duplicate colors for Product ID 4 (Streetwear Hoodie)
print("Removing duplicates for Product ID 4 (Streetwear Hoodie)...")
cur.execute("DELETE FROM product_colors WHERE id IN (27, 28, 29)")
print(f"Deleted {cur.rowcount} duplicate colors")

# Remove duplicate colors for Product ID 6 (Half-Zip Sweatshirt)
print("Removing duplicates for Product ID 6 (Half-Zip Sweatshirt)...")
cur.execute("DELETE FROM product_colors WHERE id IN (30, 31, 32)")
print(f"Deleted {cur.rowcount} duplicate colors")

con.commit()

print("\n=== ADDING COLORS FOR COUPLE COORDINATED OUTFIT ===")
# Add colors for Product ID 18 (Couple Coordinated Outfit)
print("Adding colors for Product ID 18 (Couple Coordinated Outfit)...")
cur.execute("""
    INSERT INTO product_colors (product_id, color, color_image) VALUES
    (18, 'brown', 'brown_couple-outfit.png'),
    (18, 'gray', 'gray_couple-outfit.png')
""")
print(f"Added {cur.rowcount} colors")

con.commit()

print("\n=== VERIFICATION ===")
cur.execute("""
    SELECT p.id, p.name, COUNT(pc.id) as color_count
    FROM products p
    LEFT JOIN product_colors pc ON p.id = pc.product_id
    WHERE p.id IN (3, 4, 6, 18)
    GROUP BY p.id, p.name
    ORDER BY p.id
""")
products = cur.fetchall()
for prod in products:
    print(f"Product ID: {prod[0]}, Name: {prod[1]}, Colors: {prod[2]}")

cur.close()
con.close()

print("\n✅ All duplicates removed and missing colors added!")
