import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="trendify_db",
        port=3306
    )

try:
    con = get_connection()
    cur = con.cursor()
    
    # Check if color_id column exists
    cur.execute("SHOW COLUMNS FROM cart LIKE 'color_id'")
    result = cur.fetchone()
    
    if not result:
        print("Adding color_id column to cart table...")
        cur.execute("ALTER TABLE cart ADD COLUMN color_id INT")
        con.commit()
        print("✓ color_id column added successfully!")
    else:
        print("✓ color_id column already exists in cart table")
    
    # Check if size column exists
    cur.execute("SHOW COLUMNS FROM cart LIKE 'size'")
    result = cur.fetchone()
    
    if not result:
        print("Adding size column to cart table...")
        cur.execute("ALTER TABLE cart ADD COLUMN size VARCHAR(10)")
        con.commit()
        print("✓ size column added successfully!")
    else:
        print("✓ size column already exists in cart table")
    
    # Clear existing cart data to avoid conflicts
    print("Clearing existing cart data...")
    cur.execute("DELETE FROM cart")
    con.commit()
    print("✓ Cart cleared - you can now add products with color and size variants!")
    
    cur.close()
    con.close()
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure MySQL is running and database exists")