from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import re
import razorpay
import hmac
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_CONFIG, FLASK_CONFIG, SECRET_KEY, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

app = Flask(__name__)
app.secret_key = SECRET_KEY

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# ================= DATABASE CONNECTION =================
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ================= SESSION CART INIT =================
def init_session_cart():
    if "cart" not in session:
        session["cart"] = {}

# ================= MERGE SESSION CART INTO DB =================
def merge_cart_to_db(user_id):
    if "cart" not in session:
        return

    con = get_connection()
    cur = con.cursor()

    for product_id, qty in session["cart"].items():
        cur.execute("""
            SELECT id FROM cart
            WHERE user_id=%s AND product_id=%s
        """, (user_id, product_id))

        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE cart
                SET quantity = quantity + %s
                WHERE user_id=%s AND product_id=%s
            """, (qty, user_id, product_id))
        else:
            cur.execute("""
                INSERT INTO cart (user_id, product_id, quantity)
                VALUES (%s,%s,%s)
            """, (user_id, product_id, qty))

    con.commit()
    cur.close()
    con.close()

    session.pop("cart", None)

# ================= HOME =================
@app.route("/")
def home():
    products = fetch_products()
    return render_template("base.html", products=products)

# ================= COMMON PRODUCT FETCH FUNCTION =================
def fetch_products(where_clause="", params=()):
    con = get_connection()
    cur = con.cursor(dictionary=True)

    query = f"""
        SELECT 
            p.id AS product_id,
            p.name,
            p.price,
            p.description,
            p.quality,
            p.quantity,
            p.size,
            p.image,
            p.category_id,
            pc.id AS color_id,
            pc.color,
            pc.color_image
        FROM products p
        LEFT JOIN product_colors pc ON p.id = pc.product_id
        {where_clause}
        ORDER BY p.id;
    """

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    con.close()

    products_dict = {}

    for row in rows:
        pid = row["product_id"]

        if pid not in products_dict:
            products_dict[pid] = {
                "id": pid,
                "name": row["name"],
                "price": row["price"],
                "description": row["description"],
                "quality": row["quality"],
                "quantity": row["quantity"],
                "size": row["size"],
                "image": row["image"],
                "category_id": row["category_id"],
                "colors": []
            }

        if row["color_id"] is not None:
            products_dict[pid]["colors"].append({
                "id": row["color_id"],
                "color": row["color"],
                "color_image": row["color_image"]
            })

    return list(products_dict.values())


# ================= SEARCH =================
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    products = []
    if query:
        products = fetch_products("WHERE p.name LIKE %s", (f"%{query}%",))
    return render_template("search.html", products=products, query=query)

# ================= TRENDING =================
@app.route("/trending")
def trending():
    products = fetch_products("WHERE category_id=%s", (1,))
    return render_template("trending.html", products=products)

# ================= OCCASION =================
@app.route("/occasion")
def occasion():
    products = fetch_products("WHERE category_id=%s", (2,))
    return render_template("occasion.html", products=products)

# ================= MOST SELLING =================
@app.route("/mostselling")
def mostselling():
    con = get_connection()
    cur = con.cursor(dictionary=True)

    # Get most selling products with their details
    cur.execute("""
        SELECT p.id, p.name, p.price, p.description, p.quality,
               m.image,
               m.size
        FROM most_selling_products m
        JOIN products p ON m.product_id = p.id
    """)

    products_list = cur.fetchall()
    
    # Get colors for each product
    for product in products_list:
        cur.execute("""
            SELECT id, color, color_image 
            FROM product_colors 
            WHERE product_id = %s
        """, (product['id'],))
        product['colors'] = cur.fetchall()

    cur.close()
    con.close()

    return render_template("mostselling.html", products=products_list)

# ================= PRODUCT DETAILS =================
@app.route("/product/<int:product_id>")
def product_details(product_id):
    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()

    if not product:
        cur.close()
        con.close()
        return "Product Not Found!", 404

    cur.execute("SELECT * FROM product_colors WHERE product_id=%s", (product_id,))
    colors = cur.fetchall()

    # Fetch product images for gallery
    cur.execute("SELECT * FROM product_images WHERE product_id=%s ORDER BY display_order", (product_id,))
    product_images = cur.fetchall()

    cur.close()
    con.close()

    product["colors"] = colors
    product["gallery_images"] = product_images
    product["specifications"] = []
    return render_template("product_details.html", product=product)
# ================= ADD TO CART (NO LOGIN REQUIRED) =================
@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    quantity = 1
    color_id = request.form.get("color_id")  # Get selected color
    size = request.form.get("size")  # Get selected size

    # If user logged in → store in DB
    if "user_id" in session:
        user_id = session["user_id"]
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT id FROM cart
            WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
        """, (user_id, product_id, color_id, size))

        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE cart
                SET quantity = quantity + 1
                WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
            """, (user_id, product_id, color_id, size))
        else:
            cur.execute("""
                INSERT INTO cart (user_id, product_id, quantity, color_id, size)
                VALUES (%s,%s,%s,%s,%s)
            """, (user_id, product_id, quantity, color_id, size))

        con.commit()
        cur.close()
        con.close()

    # If guest user → store in session
    else:
        init_session_cart()
        cart = session["cart"]
        cart_key = f"{product_id}_{color_id}_{size}" if color_id and size else str(product_id)
        cart[cart_key] = cart.get(cart_key, 0) + 1
        session["cart"] = cart

    flash("Product added to cart!", "success")
    return redirect(url_for("cart"))

# ================= REMOVE FROM CART =================
@app.route("/remove_from_cart/<int:product_id>")
@app.route("/remove_from_cart/<int:product_id>/<int:color_id>/<size>")
def remove_from_cart(product_id, color_id=None, size=None):

    # If logged in → remove from DB
    if "user_id" in session:
        user_id = session["user_id"]

        con = get_connection()
        cur = con.cursor()

        if color_id is not None and size is not None:
            # Remove specific variant
            cur.execute("""
                DELETE FROM cart
                WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
            """, (user_id, product_id, color_id, size))
            print(f"Removing: user_id={user_id}, product_id={product_id}, color_id={color_id}, size={size}")
        else:
            # Remove all variants of this product
            cur.execute("""
                DELETE FROM cart
                WHERE user_id=%s AND product_id=%s
            """, (user_id, product_id))
            print(f"Removing all variants: user_id={user_id}, product_id={product_id}")

        affected_rows = cur.rowcount
        con.commit()
        cur.close()
        con.close()
        
        print(f"Rows affected: {affected_rows}")

    # If guest → remove from session cart
    else:
        if "cart" in session:
            cart = session["cart"]
            removed = False
            
            if color_id is not None and size is not None:
                cart_key = f"{product_id}_{color_id}_{size}"
                if cart_key in cart:
                    cart.pop(cart_key)
                    removed = True
                    print(f"Removed from session: {cart_key}")
            
            # Also try to remove by product_id only (fallback)
            if not removed:
                keys_to_remove = []
                for key in cart.keys():
                    if key.startswith(str(product_id)):
                        keys_to_remove.append(key)
                
                for key in keys_to_remove:
                    cart.pop(key)
                    removed = True
                    print(f"Removed from session (fallback): {key}")
            
            session["cart"] = cart
            session.modified = True

    flash("Item removed from cart!", "success")
    return redirect(url_for("cart"))

# ================= REMOVE FROM CART BY KEY =================
@app.route("/remove_cart_item/<cart_key>")
def remove_cart_item(cart_key):
    if "cart" in session:
        cart = session["cart"]
        if cart_key in cart:
            cart.pop(cart_key)
            session["cart"] = cart
            session.modified = True
            flash("Item removed from cart!", "success")
    return redirect(url_for("cart"))

# ================= INCREASE QUANTITY (SESSION) =================
@app.route("/increase_quantity/<cart_key>")
def increase_quantity(cart_key):
    if "cart" in session:
        cart = session["cart"]
        if cart_key in cart:
            cart[cart_key] += 1
            session["cart"] = cart
            session.modified = True
    return redirect(url_for("cart"))

# ================= DECREASE QUANTITY (SESSION) =================
@app.route("/decrease_quantity/<cart_key>")
def decrease_quantity(cart_key):
    if "cart" in session:
        cart = session["cart"]
        if cart_key in cart:
            if cart[cart_key] > 1:
                cart[cart_key] -= 1
            else:
                cart.pop(cart_key)  # Remove if quantity becomes 0
            session["cart"] = cart
            session.modified = True
    return redirect(url_for("cart"))

# ================= INCREASE QUANTITY (DATABASE) =================
@app.route("/increase_quantity_db/<int:product_id>")
@app.route("/increase_quantity_db/<int:product_id>/<int:color_id>/<size>")
def increase_quantity_db(product_id, color_id=None, size=None):
    if "user_id" in session:
        user_id = session["user_id"]
        con = get_connection()
        cur = con.cursor()

        if color_id is not None and size is not None:
            cur.execute("""
                UPDATE cart SET quantity = quantity + 1
                WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
            """, (user_id, product_id, color_id, size))
        else:
            cur.execute("""
                UPDATE cart SET quantity = quantity + 1
                WHERE user_id=%s AND product_id=%s
            """, (user_id, product_id))

        con.commit()
        cur.close()
        con.close()
    
    return redirect(url_for("cart"))

# ================= DECREASE QUANTITY (DATABASE) =================
@app.route("/decrease_quantity_db/<int:product_id>")
@app.route("/decrease_quantity_db/<int:product_id>/<int:color_id>/<size>")
def decrease_quantity_db(product_id, color_id=None, size=None):
    if "user_id" in session:
        user_id = session["user_id"]
        con = get_connection()
        cur = con.cursor()

        if color_id is not None and size is not None:
            # Check current quantity
            cur.execute("""
                SELECT quantity FROM cart
                WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
            """, (user_id, product_id, color_id, size))
            
            result = cur.fetchone()
            if result and result[0] > 1:
                cur.execute("""
                    UPDATE cart SET quantity = quantity - 1
                    WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
                """, (user_id, product_id, color_id, size))
            else:
                cur.execute("""
                    DELETE FROM cart
                    WHERE user_id=%s AND product_id=%s AND color_id=%s AND size=%s
                """, (user_id, product_id, color_id, size))
        else:
            # Check current quantity
            cur.execute("""
                SELECT quantity FROM cart
                WHERE user_id=%s AND product_id=%s
            """, (user_id, product_id))
            
            result = cur.fetchone()
            if result and result[0] > 1:
                cur.execute("""
                    UPDATE cart SET quantity = quantity - 1
                    WHERE user_id=%s AND product_id=%s
                """, (user_id, product_id))
            else:
                cur.execute("""
                    DELETE FROM cart
                    WHERE user_id=%s AND product_id=%s
                """, (user_id, product_id))

        con.commit()
        cur.close()
        con.close()
    
    return redirect(url_for("cart"))

# ================= CART =================
@app.route("/cart")
def cart():
    cart_items = []
    grand_total = 0

    # Logged-in user cart from DB
    if "user_id" in session:
        user_id = session["user_id"]
        con = get_connection()
        cur = con.cursor(dictionary=True)

        cur.execute("""
            SELECT p.id, p.name, p.price, 
                   COALESCE(pc.color_image, p.image) as image, 
                   c.quantity,
                   pc.color,
                   pc.id as color_id,
                   c.size
            FROM cart c
            JOIN products p ON c.product_id = p.id
            LEFT JOIN product_colors pc ON c.color_id = pc.id
            WHERE c.user_id=%s
        """, (user_id,))

        cart_items = cur.fetchall()

        cur.close()
        con.close()

    # Guest user cart from session
    else:
        init_session_cart()
        con = get_connection()
        cur = con.cursor(dictionary=True)

        for cart_key, qty in session["cart"].items():
            product = None
            if "_" in cart_key:
                parts = cart_key.split("_")
                if len(parts) == 3:  # product_id_color_id_size
                    product_id, color_id, size = parts
                    cur.execute("""
                        SELECT p.id, p.name, p.price, pc.color_image as image, pc.color, pc.id as color_id
                        FROM products p
                        JOIN product_colors pc ON p.id = pc.product_id
                        WHERE p.id=%s AND pc.id=%s
                    """, (product_id, color_id))
                    product = cur.fetchone()
                    if product:
                        product["size"] = size
                        product["cart_key"] = cart_key
                elif len(parts) == 2:  # product_id_color_id (backward compatibility)
                    product_id, color_id = parts
                    cur.execute("""
                        SELECT p.id, p.name, p.price, pc.color_image as image, pc.color, pc.id as color_id
                        FROM products p
                        JOIN product_colors pc ON p.id = pc.product_id
                        WHERE p.id=%s AND pc.id=%s
                    """, (product_id, color_id))
                    product = cur.fetchone()
                    if product:
                        product["cart_key"] = cart_key
            else:
                product_id = cart_key
                cur.execute("SELECT id,name,price,image FROM products WHERE id=%s", (product_id,))
                product = cur.fetchone()
                if product:
                    product["cart_key"] = cart_key
            
            if product:
                product["quantity"] = qty
                cart_items.append(product)

        cur.close()
        con.close()

    for item in cart_items:
        item["total"] = item["price"] * item["quantity"]
        grand_total += item["total"]

    return render_template("cart.html",
                           cart_items=cart_items,
                           grand_total=grand_total)

# ================= SIGNUP =================
# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        gender = request.form["gender"]
        age = request.form["age"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        # Validate username format (only letters, numbers, underscores, 3-20 chars)
        username_pattern = r'^[a-zA-Z0-9_]{3,20}$'
        if not re.match(username_pattern, username):
            flash("Username must be 3-20 characters and contain only letters, numbers, and underscores!", "danger")
            return render_template("signup.html")
        
        # Validate email format
        # Must start with alphanumeric, no consecutive dots, valid domain
        email_pattern = r'^[a-zA-Z0-9]+[a-zA-Z0-9._-]*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,3}$'
        if not re.match(email_pattern, email) or '..' in email or email.startswith('.') or email.endswith('.'):
            flash("Please enter a valid email address!", "danger")
            return render_template("signup.html")
        
        # Check for consecutive dots
        if '..' in email:
            flash("Email cannot contain consecutive dots!", "danger")
            return render_template("signup.html")
        
        # Check if email starts with dot
        if email.startswith('.'):
            flash("Email cannot start with a dot!", "danger")
            return render_template("signup.html")
        
        # Validate phone number
        if not phone or len(phone) != 10 or not phone.isdigit():
            flash("Phone number must be exactly 10 digits!", "danger")
            return render_template("signup.html")
        
        # Validate password match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template("signup.html")
        
        # Hash password
        hashed_password = generate_password_hash(password)

        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute("""
                INSERT INTO users(username, email, phone, gender, age, password) 
                VALUES(%s, %s, %s, %s, %s, %s)
            """, (username, email, phone, gender, age, hashed_password))

            con.commit()
            
            # Auto-login after signup
            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cur.fetchone()
            
            if user:
                session["user_id"] = user[0]  # user id
                session["username"] = user[1]  # username
                
                merge_cart_to_db(user[0])
                
                flash("Signup successful! You are now logged in.", "success")
                
                # Redirect to the page user was trying to access
                next_url = session.pop("next_url", None)
                if next_url:
                    return redirect(next_url)
                return redirect(url_for("home"))
            else:
                flash("Signup successful! Please login.", "success")
                return redirect(url_for("login"))
            
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return render_template("signup.html")
        
        finally:
            cur.close()
            con.close()

    return render_template("signup.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = get_connection()
        cur = con.cursor(dictionary=True)

        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        cur.close()
        con.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            merge_cart_to_db(user["id"])

            flash("Login successful!", "success")
            
            # Redirect to the page user was trying to access
            next_url = session.pop("next_url", None)
            if next_url:
                return redirect(next_url)
            return redirect(url_for("home"))

        flash("Invalid credentials!", "danger")

    return render_template("login.html")

# ================= FORGOT PASSWORD =================
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        step = request.form.get("step")

        if step == "verify":
            email = request.form["email"].strip().lower()
            phone = request.form["phone"].strip()

            con = get_connection()
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT id FROM users WHERE email=%s AND phone=%s", (email, phone))
            user = cur.fetchone()
            cur.close()
            con.close()

            if user:
                session["reset_user_id"] = user["id"]
                next_page = request.form.get("next", "login")
                return render_template("forgot_password.html", step="reset", next=next_page)
            else:
                flash("No account found with that email and phone combination!", "danger")
                next_page = request.form.get("next", "login")
                return render_template("forgot_password.html", step="verify", next=next_page)

        elif step == "reset":
            if "reset_user_id" not in session:
                flash("Session expired. Please try again.", "danger")
                return redirect(url_for("forgot_password"))

            new_pw = request.form["new_password"]
            confirm_pw = request.form["confirm_password"]
            next_page = request.form.get("next", "login")

            if new_pw != confirm_pw:
                flash("Passwords do not match!", "danger")
                return render_template("forgot_password.html", step="reset", next=next_page)
            if len(new_pw) < 6:
                flash("Password must be at least 6 characters!", "danger")
                return render_template("forgot_password.html", step="reset", next=next_page)

            con = get_connection()
            cur = con.cursor()
            cur.execute("UPDATE users SET password=%s WHERE id=%s",
                        (generate_password_hash(new_pw), session["reset_user_id"]))
            con.commit()
            cur.close()
            con.close()

            session.pop("reset_user_id", None)
            flash("Password reset successfully!", "success")

            if next_page == "profile":
                return redirect(url_for("profile"))
            return redirect(url_for("login"))

    next_page = request.args.get("next", "login")
    return render_template("forgot_password.html", step="verify", next=next_page)

# ================= PROFILE =================
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        flash("Please login to view your profile!", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    con = get_connection()
    cur = con.cursor(dictionary=True)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "update_info":
            username = request.form["username"].strip()
            phone = request.form["phone"].strip()

            # Allow letters and spaces only, between 2 and 20 characters
            if not re.match(r'^[a-zA-Z ]{2,20}$', username):
                flash("Name must be 2–20 characters, letters and spaces only.", "danger")
            elif not re.match(r'^[0-9]{10}$', phone):
                flash("Phone must be exactly 10 digits!", "danger")
            else:
                try:
                    # Check if phone is already used by another user
                    cur.execute("SELECT id FROM users WHERE phone=%s AND id != %s", (phone, user_id))
                    if cur.fetchone():
                        flash("This phone number is already registered with another account!", "danger")
                    else:
                        cur.execute("UPDATE users SET username=%s, phone=%s WHERE id=%s",
                                    (username, phone, user_id))
                        con.commit()
                        session["username"] = username
                        flash("Profile updated successfully!", "success")
                except Exception as e:
                    flash("Something went wrong. Please try again.", "danger")

        elif action == "change_password":
            current_pw = request.form["current_password"]
            new_pw = request.form["new_password"]
            confirm_pw = request.form["confirm_password"]

            cur.execute("SELECT password FROM users WHERE id=%s", (user_id,))
            user = cur.fetchone()

            if not check_password_hash(user["password"], current_pw):
                flash("Current password is incorrect!", "danger")
            elif new_pw != confirm_pw:
                flash("New passwords do not match!", "danger")
            elif len(new_pw) < 6:
                flash("New password must be at least 6 characters!", "danger")
            else:
                cur.execute("UPDATE users SET password=%s WHERE id=%s",
                            (generate_password_hash(new_pw), user_id))
                con.commit()
                flash("Password changed successfully!", "success")

    cur.execute("SELECT id, username, email, phone, gender, age, created_at FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()
    con.close()

    return render_template("profile.html", user=user)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

# ================= TERMS AND CONDITIONS =================
@app.route("/terms")
def terms():
    return render_template("terms.html")

# ================= PRIVACY POLICY =================
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ================= RETURN AND REFUND POLICY =================
@app.route("/returns")
def returns():
    return render_template("returns.html")

# ================= SHIPPING POLICY =================
@app.route("/shipping")
def shipping():
    return render_template("shipping.html")

# ================= ABOUT US =================
@app.route("/about")
def about():
    return render_template("about.html")

# ================= CONTACT US =================
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ================= FAQ =================
@app.route("/faq")
def faq():
    return render_template("faq.html")

# ================= SECURITY POLICY =================
@app.route("/security")
def security():
    return render_template("security.html")

# ================= PAYMENT POLICY =================
@app.route("/payments")
def payments():
    return render_template("payments.html")

# ================= CAREERS =================
@app.route("/careers")
def careers():
    return render_template("careers.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        rating = request.form.get("rating", "").strip()
        message = request.form["message"].strip()

        # Validate email - strict check
        email_pattern = r'^[a-zA-Z0-9]+[a-zA-Z0-9._-]*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,3}$'
        if not re.match(email_pattern, email) or '..' in email or email.startswith('.') or email.endswith('.'):
            flash("Please enter a valid email address!", "error")
            return render_template("feedback.html")

        # Validate rating
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash("Please select a valid rating!", "error")
            return render_template("feedback.html")

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO feedback (name, email, rating, message) 
            VALUES (%s, %s, %s, %s)
        """, (name, email, int(rating), message))

        con.commit()
        cur.close()
        con.close()

        flash("Thank you for your feedback! We appreciate your input.", "success")
        return redirect(url_for("feedback"))

    return render_template("feedback.html")

# ================= CHECKOUT =================
@app.route("/checkout")
def checkout():
    # Check if user is logged in
    if "user_id" not in session:
        session["next_url"] = url_for("checkout")
        flash("Please login to proceed with checkout!", "warning")
        return redirect(url_for("login"))
    
    # Check if cart is not empty
    cart_items = []
    grand_total = 0
    
    user_id = session["user_id"]
    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT p.id, p.name, p.price, 
               COALESCE(pc.color_image, p.image) as image, 
               c.quantity,
               pc.color,
               pc.id as color_id,
               c.size
        FROM cart c
        JOIN products p ON c.product_id = p.id
        LEFT JOIN product_colors pc ON c.color_id = pc.id
        WHERE c.user_id=%s
    """, (user_id,))

    cart_items = cur.fetchall()
    cur.close()
    con.close()

    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("cart"))

    for item in cart_items:
        item["total"] = item["price"] * item["quantity"]
        grand_total += item["total"]

    return render_template("checkout.html", 
                           cart_items=cart_items, 
                           grand_total=grand_total)

# ================= CREATE RAZORPAY PAYMENT =================
@app.route("/create_payment", methods=["POST"])
def create_payment():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    amount = int(data.get("amount", 0)) * 100  # Razorpay uses paise

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # Store checkout form data in session for after payment
    session["pending_order"] = data
    return jsonify({"order_id": order["id"], "amount": amount, "key": RAZORPAY_KEY_ID})

# ================= VERIFY RAZORPAY PAYMENT =================
@app.route("/verify_payment", methods=["POST"])
def verify_payment():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    razorpay_order_id = data.get("razorpay_order_id")
    razorpay_payment_id = data.get("razorpay_payment_id")
    razorpay_signature = data.get("razorpay_signature")

    # Verify signature
    msg = f"{razorpay_order_id}|{razorpay_payment_id}"
    generated_sig = hmac.new(
        bytes(RAZORPAY_KEY_SECRET, 'utf-8'),
        bytes(msg, 'utf-8'),
        hashlib.sha256
    ).hexdigest()

    if generated_sig != razorpay_signature:
        return jsonify({"success": False, "error": "Payment verification failed"}), 400

    # Place the order in DB
    pending = session.get("pending_order", {})
    user_id = session["user_id"]

    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT c.*, p.price, p.name
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))
    cart_items = cur.fetchall()

    total_amount = sum(item["price"] * item["quantity"] for item in cart_items)

    cur.execute("""
        INSERT INTO orders (user_id, total_amount, payment_method, order_status)
        VALUES (%s, %s, %s, 'Confirmed')
    """, (user_id, total_amount, "Online Payment"))

    order_id = cur.lastrowid

    for item in cart_items:
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item["product_id"], item["quantity"], item["price"]))

    cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
    con.commit()
    cur.close()
    con.close()

    session.pop("pending_order", None)
    return jsonify({"success": True, "order_id": order_id})

# ================= PLACE ORDER =================
@app.route("/place_order", methods=["POST"])
def place_order():
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    payment_method = request.form.get("payment_method", "COD")
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    state = request.form.get("state", "").strip()
    pincode = request.form.get("pincode", "").strip()

    if not full_name or len(full_name) < 2:
        flash("Please enter your full name!", "danger")
        return redirect(url_for("checkout"))
    if not phone or len(phone) != 10 or not phone.isdigit():
        flash("Phone number must be exactly 10 digits!", "danger")
        return redirect(url_for("checkout"))
    if not address:
        flash("Please provide a delivery address!", "danger")
        return redirect(url_for("checkout"))
    if not city:
        flash("Please enter your city!", "danger")
        return redirect(url_for("checkout"))
    if not state:
        flash("Please select your state!", "danger")
        return redirect(url_for("checkout"))
    if not pincode or len(pincode) != 6 or not pincode.isdigit():
        flash("Pincode must be exactly 6 digits!", "danger")
        return redirect(url_for("checkout"))
    
    con = get_connection()
    cur = con.cursor(dictionary=True)
    
    # Get cart items
    cur.execute("""
        SELECT c.*, p.price, p.name
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))
    
    cart_items = cur.fetchall()
    
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("cart"))
    
    # Calculate total
    total_amount = sum(item["price"] * item["quantity"] for item in cart_items)
    
    # Create order
    cur.execute("""
        INSERT INTO orders (user_id, total_amount, payment_method, order_status)
        VALUES (%s, %s, %s, 'Pending')
    """, (user_id, total_amount, payment_method))
    
    order_id = cur.lastrowid
    
    # Add order items
    for item in cart_items:
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item["product_id"], item["quantity"], item["price"]))
    
    # Clear cart
    cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
    
    con.commit()
    cur.close()
    con.close()
    
    flash(f"Order #{order_id} placed successfully!", "success")
    return redirect(url_for("order_success", order_id=order_id))

# ================= ORDER SUCCESS =================
@app.route("/order_success/<int:order_id>")
def order_success(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    
    con = get_connection()
    cur = con.cursor(dictionary=True)
    
    cur.execute("""
        SELECT * FROM orders 
        WHERE id=%s AND user_id=%s
    """, (order_id, user_id))
    
    order = cur.fetchone()
    cur.close()
    con.close()
    
    if not order:
        flash("Order not found!", "danger")
        return redirect(url_for("home"))
    
    return render_template("order_success.html", order=order)

# ================= RETURN ORDER =================
@app.route("/return_order/<int:order_id>", methods=["GET", "POST"])
def return_order(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("SELECT * FROM orders WHERE id=%s AND user_id=%s", (order_id, user_id))
    order = cur.fetchone()

    if not order or order["order_status"] != "Delivered":
        flash("Only delivered orders can be returned!", "danger")
        cur.close()
        con.close()
        return redirect(url_for("my_orders"))

    if request.method == "POST":
        reason = request.form.get("reason", "").strip()
        if not reason:
            flash("Please provide a reason for return!", "danger")
            cur.close()
            con.close()
            return render_template("return_order.html", order=order)

        # Check if return already requested
        cur.execute("SELECT id FROM return_requests WHERE order_id=%s", (order_id,))
        existing = cur.fetchone()
        if existing:
            flash("Return request already submitted for this order!", "warning")
        else:
            cur.execute("""
                INSERT INTO return_requests (order_id, user_id, reason)
                VALUES (%s, %s, %s)
            """, (order_id, user_id, reason))
            cur.execute("UPDATE orders SET order_status='Return Requested' WHERE id=%s", (order_id,))
            con.commit()
            flash("Return request submitted successfully! We will contact you soon.", "success")

        cur.close()
        con.close()
        return redirect(url_for("my_orders"))

    cur.close()
    con.close()
    return render_template("return_order.html", order=order)

# ================= CANCEL ORDER =================
@app.route("/cancel_order/<int:order_id>", methods=["POST"])
def cancel_order(order_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    con = get_connection()
    cur = con.cursor(dictionary=True)

    # Make sure order belongs to this user and is still Pending
    cur.execute("SELECT id, order_status FROM orders WHERE id=%s AND user_id=%s", (order_id, user_id))
    order = cur.fetchone()

    if not order:
        flash("Order not found!", "danger")
    elif order["order_status"] == "Delivered":
        flash("Delivered orders cannot be cancelled. Please use the Return option!", "danger")
    elif order["order_status"] == "Cancelled":
        flash("This order is already cancelled!", "danger")
    else:
        cur.execute("UPDATE orders SET order_status='Cancelled' WHERE id=%s", (order_id,))
        con.commit()
        flash("Order cancelled successfully!", "success")

    cur.close()
    con.close()
    return redirect(url_for("my_orders"))

# ================= ORDER HISTORY =================
@app.route("/my_orders")
def my_orders():
    if "user_id" not in session:
        flash("Please login to view your orders!", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT o.id, o.total_amount, o.order_status, o.payment_method, o.order_date,
               p.id as product_id, p.name as product_name, p.image as product_image,
               oi.quantity, oi.price
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC, o.id DESC
    """, (user_id,))

    rows = cur.fetchall()
    cur.close()
    con.close()

    # Group rows by order id
    grouped = {}
    for row in rows:
        oid = row["id"]
        if oid not in grouped:
            grouped[oid] = {
                "id": row["id"],
                "total_amount": row["total_amount"],
                "order_status": row["order_status"],
                "payment_method": row["payment_method"],
                "order_date": row["order_date"],
                "products": []
            }
        if row["product_name"]:
            grouped[oid]["products"].append({
                "id": row["product_id"],
                "name": row["product_name"],
                "image": row["product_image"],
                "quantity": row["quantity"],
                "price": row["price"]
            })

    purchase_list = list(grouped.values())
    return render_template("my_orders.html", purchase_list=purchase_list)

# ================= ADMIN ROUTES =================

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please login as admin first!", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# Admin Login
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cur.fetchone()
        cur.close()
        con.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            flash("Admin login successful!", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid admin credentials!", "danger")

    return render_template("admin/admin_login.html")

# Admin Dashboard
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) as total FROM products")
    total_products = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) as total FROM users")
    total_users = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) as total FROM cart")
    total_cart_items = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) as total FROM orders")
    total_orders = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) as total FROM product_colors")
    total_colors = cur.fetchone()["total"]

    cur.close()
    con.close()

    return render_template("admin/admin_dashboard.html",
                           total_products=total_products,
                           total_users=total_users,
                           total_cart_items=total_cart_items,
                           total_orders=total_orders,
                           total_colors=total_colors)

# Admin Products List
@app.route("/admin/products")
@admin_required
def admin_products():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    products = cur.fetchall()
    cur.close()
    con.close()

    return render_template("admin/admin_products.html", products=products)

# Admin Add Product
@app.route("/admin/products/add", methods=["GET", "POST"])
@admin_required
def admin_add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        quality = request.form["quality"]
        quantity = request.form["quantity"]
        size = request.form["size"]
        image = request.form["image"]
        category_id = request.form["category_id"]

        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO products (name, price, description, quality, quantity, size, image, category_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, price, description, quality, quantity, size, image, category_id))
        
        product_id = cur.lastrowid
        con.commit()
        cur.close()
        con.close()

        flash(f"Product '{name}' added successfully! Now you can add color variants.", "success")
        return redirect(url_for("admin_colors"))

    return render_template("admin/admin_add_product.html")

# Admin Edit Product
@app.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_product(product_id):
    con = get_connection()
    cur = con.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        quality = request.form["quality"]
        quantity = request.form["quantity"]
        size = request.form["size"]
        image = request.form["image"]
        category_id = request.form["category_id"]

        cur.execute("""
            UPDATE products
            SET name=%s, price=%s, description=%s, quality=%s, quantity=%s, size=%s, image=%s, category_id=%s
            WHERE id=%s
        """, (name, price, description, quality, quantity, size, image, category_id, product_id))
        con.commit()
        cur.close()
        con.close()

        flash("Product updated successfully!", "success")
        return redirect(url_for("admin_products"))

    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()
    cur.close()
    con.close()

    return render_template("admin/admin_edit_product.html", product=product)

# Admin Delete Product
@app.route("/admin/products/delete/<int:product_id>")
@admin_required
def admin_delete_product(product_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
    con.commit()
    cur.close()
    con.close()

    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin_products"))

# Admin Users List
@app.route("/admin/users")
@admin_required
def admin_users():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT id, username, email, phone, gender, age, created_at FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close()
    con.close()

    return render_template("admin/admin_users.html", users=users)

@app.route("/admin/feedback")
@admin_required
def admin_feedback():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM feedback ORDER BY created_at DESC")
    feedbacks = cur.fetchall()
    cur.close()
    con.close()
    return render_template("admin/admin_feedback.html", feedbacks=feedbacks)

@app.route("/admin/feedback/delete/<int:feedback_id>", methods=["POST"])
@admin_required
def admin_delete_feedback(feedback_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM feedback WHERE id=%s", (feedback_id,))
    con.commit()
    cur.close()
    con.close()
    flash("Feedback deleted successfully!", "success")
    return redirect(url_for("admin_feedback"))

# Admin Colors List
@app.route("/admin/colors")
@admin_required
def admin_colors():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT pc.*, p.name as product_name 
        FROM product_colors pc
        JOIN products p ON pc.product_id = p.id
        ORDER BY pc.product_id, pc.id
    """)
    colors = cur.fetchall()
    cur.close()
    con.close()

    return render_template("admin/admin_colors.html", colors=colors)

# Admin Add Color
@app.route("/admin/colors/add", methods=["GET", "POST"])
@admin_required
def admin_add_color():
    if request.method == "POST":
        product_id = request.form["product_id"]
        color = request.form["color"]
        color_image = request.form["color_image"]

        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO product_colors (product_id, color, color_image)
            VALUES (%s, %s, %s)
        """, (product_id, color, color_image))
        con.commit()
        cur.close()
        con.close()

        flash("Color added successfully!", "success")
        return redirect(url_for("admin_colors"))

    # Get products for dropdown
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM products ORDER BY name")
    products = cur.fetchall()
    cur.close()
    con.close()

    return render_template("admin/admin_add_color.html", products=products)

# Admin Delete Color
@app.route("/admin/colors/delete/<int:color_id>")
@admin_required
def admin_delete_color(color_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM product_colors WHERE id=%s", (color_id,))
    con.commit()
    cur.close()
    con.close()

    flash("Color deleted successfully!", "success")
    return redirect(url_for("admin_colors"))

# Admin Orders List
@app.route("/admin/orders")
@admin_required
def admin_orders():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT o.*, u.username 
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.order_date DESC
    """)
    orders = cur.fetchall()
    cur.close()
    con.close()

    return render_template("admin/admin_orders.html", orders=orders)

# Admin Order Details
@app.route("/admin/orders/<int:order_id>")
@admin_required
def admin_order_details(order_id):
    con = get_connection()
    cur = con.cursor(dictionary=True)
    
    # Get order info
    cur.execute("""
        SELECT o.*, u.username 
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = %s
    """, (order_id,))
    order = cur.fetchone()
    
    # Get order items
    cur.execute("""
        SELECT oi.*, p.name, p.image
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    """, (order_id,))
    order_items = cur.fetchall()
    
    cur.close()
    con.close()

    return render_template("admin/admin_order_details.html", order=order, order_items=order_items)

# Admin Update Order Status
@app.route("/admin/orders/update_status/<int:order_id>", methods=["POST"])
@admin_required
def admin_update_order_status(order_id):
    new_status = request.form["status"]

    con = get_connection()
    cur = con.cursor(dictionary=True)

    # Block update if order is already Cancelled
    cur.execute("SELECT order_status FROM orders WHERE id=%s", (order_id,))
    order = cur.fetchone()

    if order and order["order_status"] == "Cancelled":
        flash("Cannot update a cancelled order!", "danger")
        cur.close()
        con.close()
        return redirect(url_for("admin_order_details", order_id=order_id))

    cur.execute("UPDATE orders SET order_status = %s WHERE id = %s", (new_status, order_id))
    con.commit()
    cur.close()
    con.close()

    flash("Order status updated successfully!", "success")
    return redirect(url_for("admin_order_details", order_id=order_id))

# ================= ADMIN RETURN REQUESTS =================
@app.route("/admin/returns")
@admin_required
def admin_returns():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT rr.id, rr.order_id, rr.reason, rr.refund_status, rr.admin_note, rr.requested_at,
               u.username, o.total_amount, o.payment_method
        FROM return_requests rr
        JOIN users u ON rr.user_id = u.id
        JOIN orders o ON rr.order_id = o.id
        ORDER BY rr.requested_at DESC
    """)
    return_list = cur.fetchall()
    cur.close()
    con.close()
    return render_template("admin/admin_returns.html", return_list=return_list)

@app.route("/admin/returns/update/<int:return_id>", methods=["POST"])
@admin_required
def admin_update_return(return_id):
    refund_status = request.form.get("refund_status")
    admin_note = request.form.get("admin_note", "").strip()

    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("UPDATE return_requests SET refund_status=%s, admin_note=%s WHERE id=%s",
                (refund_status, admin_note, return_id))

    # Update order status based on refund decision
    cur.execute("SELECT order_id FROM return_requests WHERE id=%s", (return_id,))
    row = cur.fetchone()
    if row:
        if refund_status == "Approved":
            cur.execute("UPDATE orders SET order_status='Refund Approved' WHERE id=%s", (row["order_id"],))
        elif refund_status == "Rejected":
            cur.execute("UPDATE orders SET order_status='Return Rejected' WHERE id=%s", (row["order_id"],))

    con.commit()
    cur.close()
    con.close()
    flash("Return request updated!", "success")
    return redirect(url_for("admin_returns"))

# Admin Logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    flash("Admin logged out successfully!", "success")
    return redirect(url_for("admin_login"))

# Admin to Website (Auto-login test user)
@app.route("/admin/goto_website")
@admin_required
def admin_goto_website():
    # Auto-login test user for demo purposes
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username = 'testuser'")
    user = cur.fetchone()
    cur.close()
    con.close()
    
    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash("Logged in as test user for demo!", "info")
    
    return redirect(url_for("home"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(
        host=FLASK_CONFIG["host"],
        port=FLASK_CONFIG["port"],
        debug=FLASK_CONFIG["debug"]
    )