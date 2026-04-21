import mysql.connector

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="trendify_db",
    port=3306
)

cur = con.cursor()

print("Fixing most_selling_products table...\n")

# Add size column if missing
try:
    cur.execute("""
        ALTER TABLE most_selling_products 
        ADD COLUMN size VARCHAR(50) DEFAULT NULL
    """)
    print("✓ Added size column")
except Exception as e:
    print(f"  size column: {e}")

con.commit()

# Clear existing data
cur.execute("DELETE FROM most_selling_products")
print("✓ Cleared old data")

# Insert most selling products with proper data
print("✓ Inserting most selling products...")

most_selling_data = [
    (2, 'green', 'forest_green_watch.png', 'One Size'),
    (4, 'brown', 'brown_hoodie.png', 'S,M,L,XL,XXL'),
    (5, 'white', 'sneakers.jpg', '7,8,9,10,12'),
    (6, 'brown', 'brown_sweat.png', 'S,M,L,XL,XXL'),
    (12, 'purple', 'p1.png', 'S,M,L,XL,XXL'),
    (13, 'black', 'sarii.jpg', 'Free Size'),
    (15, 'pink', 'pink2.png', 'S,M,L,XL,XXL')
]

for product_id, color, image, size in most_selling_data:
    try:
        cur.execute("""
            INSERT INTO most_selling_products (product_id, color, image, size)
            VALUES (%s, %s, %s, %s)
        """, (product_id, color, image, size))
        print(f"  Added product_id {product_id}")
    except Exception as e:
        print(f"  Error adding product_id {product_id}: {e}")

con.commit()

# Verify
cur.execute("DESCRIBE most_selling_products")
columns = cur.fetchall()

print("\nUpdated table structure:")
for col in columns:
    print(f"  {col[0]} - {col[1]}")

cur.execute("SELECT COUNT(*) FROM most_selling_products")
count = cur.fetchone()[0]
print(f"\nTotal products: {count}")

cur.close()
con.close()

print("\n✓ Most selling products table fixed successfully!")
