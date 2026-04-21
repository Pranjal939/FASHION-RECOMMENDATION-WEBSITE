import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="trendify_db",
        port=3306
    )

# Check products
con = get_connection()
cur = con.cursor(dictionary=True)

print("=== PRODUCTS IN DATABASE ===\n")
cur.execute("SELECT id, name, image, category_id FROM products ORDER BY id")
products = cur.fetchall()

for p in products:
    category = "Trending" if p['category_id'] == 1 else "Occasion" if p['category_id'] == 2 else "Other"
    print(f"ID: {p['id']}")
    print(f"Name: {p['name']}")
    print(f"Image: {p['image']}")
    print(f"Category: {category}")
    print("-" * 50)

cur.close()
con.close()

print("\n=== SUGGESTION ===")
print("Check if the 'image' field matches the actual product name.")
print("If brown denim jacket has 'black.jpg' as image, that's the problem!")
