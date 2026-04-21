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

# Check if table exists
cur.execute("SHOW TABLES LIKE 'most_selling_products'")
result = cur.fetchone()

if result:
    print("✓ most_selling_products table exists\n")
    
    # Check table structure
    cur.execute("DESCRIBE most_selling_products")
    columns = cur.fetchall()
    
    print("Current table structure:")
    for col in columns:
        print(f"  {col[0]} - {col[1]}")
    
    # Check data
    cur.execute("SELECT * FROM most_selling_products")
    rows = cur.fetchall()
    print(f"\nTotal rows: {len(rows)}")
else:
    print("✗ most_selling_products table does NOT exist!")

cur.close()
con.close()
