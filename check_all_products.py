import mysql.connector
from config import DB_CONFIG

con = mysql.connector.connect(**DB_CONFIG)
cur = con.cursor(dictionary=True)

cur.execute("SELECT id, name FROM products ORDER BY id")
products = cur.fetchall()

print(f"Total products in database: {len(products)}\n")
for p in products:
    print(f"ID: {p['id']}, Name: {p['name']}")

cur.close()
con.close()
