import mysql.connector
from werkzeug.security import generate_password_hash

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="trendify_db",
        port=3306
    )

# Create admins table
def create_admin_table():
    con = get_connection()
    cur = con.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    con.commit()
    cur.close()
    con.close()
    print("✓ Admins table created successfully!")

# Create admin user
def create_admin_user(username, password):
    con = get_connection()
    cur = con.cursor()
    
    hashed_password = generate_password_hash(password)
    
    try:
        cur.execute("""
            INSERT INTO admins (username, password)
            VALUES (%s, %s)
        """, (username, hashed_password))
        
        con.commit()
        print(f"✓ Admin user '{username}' created successfully!")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        
    except mysql.connector.IntegrityError:
        print(f"✗ Admin user '{username}' already exists!")
    
    cur.close()
    con.close()

if __name__ == "__main__":
    print("=== Trendify Admin Setup ===\n")
    
    # Create table
    create_admin_table()
    
    # Create default admin
    create_admin_user("admin", "admin123")
    
    print("\n=== Setup Complete ===")
    print("You can now login at: http://127.0.0.1:5000/admin/login")
