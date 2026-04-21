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

# Check cart table structure
cur.execute("DESCRIBE cart")
columns = cur.fetchall()

print("Current cart table structure:")
for col in columns:
    print(f"  {col[0]} - {col[1]}")

cur.close()
con.close()
