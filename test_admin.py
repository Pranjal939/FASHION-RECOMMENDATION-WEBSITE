import mysql.connector
from werkzeug.security import check_password_hash

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="trendify_db",
    port=3306
)

cur = con.cursor(dictionary=True)

# Check if admins table exists
cur.execute("SHOW TABLES LIKE 'admins'")
result = cur.fetchone()

if result:
    print("✓ Admins table exists")
    
    # Get all admins
    cur.execute("SELECT * FROM admins")
    admins = cur.fetchall()
    
    print(f"\nTotal admins: {len(admins)}")
    
    for admin in admins:
        print(f"\nAdmin ID: {admin['id']}")
        print(f"Username: {admin['username']}")
        print(f"Password Hash: {admin['password'][:50]}...")
        
        # Test password
        is_valid = check_password_hash(admin['password'], 'admin123')
        print(f"Password 'admin123' valid: {is_valid}")
else:
    print("✗ Admins table does NOT exist!")

cur.close()
con.close()
