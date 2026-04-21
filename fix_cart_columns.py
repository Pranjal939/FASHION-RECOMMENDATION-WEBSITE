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

print("Adding missing columns to cart table...")

try:
    # Add color_id column
    cur.execute("""
        ALTER TABLE cart 
        ADD COLUMN color_id INT DEFAULT NULL
    """)
    print("✓ Added color_id column")
except Exception as e:
    print(f"  color_id: {e}")

try:
    # Add size column
    cur.execute("""
        ALTER TABLE cart 
        ADD COLUMN size VARCHAR(50) DEFAULT NULL
    """)
    print("✓ Added size column")
except Exception as e:
    print(f"  size: {e}")

con.commit()

# Verify the changes
cur.execute("DESCRIBE cart")
columns = cur.fetchall()

print("\nUpdated cart table structure:")
for col in columns:
    print(f"  {col[0]} - {col[1]}")

cur.close()
con.close()

print("\n✓ Cart table updated successfully!")
