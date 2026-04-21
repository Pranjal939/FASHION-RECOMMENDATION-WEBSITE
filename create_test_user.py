import mysql.connector
from werkzeug.security import generate_password_hash

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
    
    # Check if test user already exists
    cur.execute("SELECT id FROM users WHERE username = 'testuser'")
    existing = cur.fetchone()
    
    if not existing:
        # Create test user
        hashed_password = generate_password_hash('test123')
        cur.execute("""
            INSERT INTO users (username, email, phone, gender, age, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ('testuser', 'test@example.com', '9876543210', 'Male', 25, hashed_password))
        
        con.commit()
        print("✓ Test user created successfully!")
        print("  Username: testuser")
        print("  Password: test123")
    else:
        print("✓ Test user already exists!")
        print("  Username: testuser")
        print("  Password: test123")
    
    cur.close()
    con.close()
    
except Exception as e:
    print(f"Error: {e}")