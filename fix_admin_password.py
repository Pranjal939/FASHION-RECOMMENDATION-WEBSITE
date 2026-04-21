import mysql.connector
from werkzeug.security import generate_password_hash

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="trendify_db",
    port=3306
)

cur = con.cursor()

# Hash the password properly
hashed_password = generate_password_hash('admin123')

# Update the admin password
cur.execute("""
    UPDATE admins 
    SET password = %s 
    WHERE username = 'admin'
""", (hashed_password,))

con.commit()

print("✓ Admin password has been properly hashed!")
print("  Username: admin")
print("  Password: admin123")
print("\nYou can now login at: http://127.0.0.1:5000/admin/login")

cur.close()
con.close()
