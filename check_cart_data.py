import mysql.connector

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="trendify_db",
    port=3306
)

cur = con.cursor(dictionary=True)

# Check cart items
cur.execute("SELECT COUNT(*) as total FROM cart")
result = cur.fetchone()
print(f"Total cart items in database: {result['total']}")

# Show cart details if any
cur.execute("SELECT * FROM cart")
carts = cur.fetchall()

if carts:
    print("\nCart items:")
    for cart in carts:
        print(f"  User ID: {cart['user_id']}, Product ID: {cart['product_id']}, Qty: {cart['quantity']}")
else:
    print("\nNo items in cart (this is normal after orders are placed)")

cur.close()
con.close()
