import mysql.connector
from config import DB_CONFIG

con = mysql.connector.connect(**DB_CONFIG)
cur = con.cursor(dictionary=True)

cur.execute("SELECT id, name FROM products WHERE name LIKE '%Shirt%' OR name LIKE '%shirt%'")
products = cur.fetchall()

for p in products:
    print(f"ID: {p['id']}, Name: {p['name']}")

cur.close()
con.close()
