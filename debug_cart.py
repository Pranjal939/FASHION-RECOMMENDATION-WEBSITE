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
    cur = con.cursor(dictionary=True)
    
    print("=== CART TABLE CONTENTS ===")
    cur.execute("SELECT * FROM cart")
    cart_items = cur.fetchall()
    
    for item in cart_items:
        print(f"ID: {item['id']}, User: {item['user_id']}, Product: {item['product_id']}, Color: {item.get('color_id')}, Size: {item.get('size')}, Qty: {item['quantity']}")
    
    if not cart_items:
        print("Cart is empty")
    
    cur.close()
    con.close()
    
except Exception as e:
    print(f"Error: {e}")