import mysql.connector
from config import DB_CONFIG

con = mysql.connector.connect(**DB_CONFIG)
cur = con.cursor()

print("=== ADDING BLUE COLOR FOR COUPLE COORDINATED OUTFIT ===")

# Add blue color using the main product image
cur.execute("""
    INSERT INTO product_colors (product_id, color, color_image) VALUES
    (18, 'blue', 'couple_outfits.jpg')
""")

con.commit()
print(f"✅ Added blue color for Couple Coordinated Outfit")

# Verify
cur.execute("""
    SELECT * FROM product_colors WHERE product_id = 18 ORDER BY id
""")
colors = cur.fetchall()
print("\n=== COLORS FOR COUPLE COORDINATED OUTFIT ===")
for color in colors:
    print(f"ID: {color[0]}, Color: {color[2]}, Image: {color[3]}")

cur.close()
con.close()
