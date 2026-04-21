# 👗 Trendify Fashion Store

A full-stack fashion e-commerce web application built using **Python Flask** and **MySQL**, designed to provide a seamless shopping experience with modern features like cart, checkout, and online payments.

---

## 🚀 Tech Stack

* **Backend:** Python Flask
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript (Vanilla)
* **Payment Gateway:** Razorpay (Test Mode)

---

## ✨ Features

### 👤 User Features

* User Signup / Login / Logout
* Forgot Password (Email + Phone Verification)
* User Profile Management (Update details, Change Password)
* Browse Products:

  * Trending
  * Occasion
  * Most Selling
* Product Details:

  * Image Gallery
  * Color Selection
  * Size Selection
  * Product Specifications
* Search Products (across all categories)
* Add to Cart (Guest + Logged-in Users)
* Checkout with Delivery Form:

  * Name, Email, Phone, Address, City, State, Pincode
* Payment Options:

  * Cash on Delivery (COD)
  * Online Payment (Razorpay – UPI, Cards)
* Order Placement & Order Success Page
* My Orders (Order History)
* Cancel Orders (Based on Status)
* Return Products (Delivered Orders)
* Feedback / Reviews with Star Rating

---

### 🛠️ Admin Panel

* Admin Login (Separate Panel)
* Dashboard Overview
* Product Management (Add, Edit, Delete)
* Product Color Management
* Order Management (View & Update Status)
* User Management
* Feedback Management
* Returns & Refund Management (Approve / Reject Requests)

---

## 📁 Project Structure

```
Trendify/
│
├── app1.py
├── config.py
├── database.sql
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── trending.html
│   ├── occasion.html
│   ├── mostselling.html
│   ├── product_details.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   ├── my_orders.html
│   ├── return_order.html
│   ├── search.html
│   ├── profile.html
│   ├── login.html
│   ├── signup.html
│   ├── forgot_password.html
│   ├── feedback.html
│   │
│   └── admin/
│       ├── admin_base.html
│       ├── admin_dashboard.html
│       ├── admin_products.html
│       ├── admin_orders.html
│       ├── admin_order_details.html
│       ├── admin_returns.html
│       ├── admin_users.html
│       └── admin_feedback.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

```bash
pip install flask mysql-connector-python werkzeug razorpay
```

---

### 2️⃣ Setup MySQL Database

```sql
CREATE DATABASE trendify_db;
USE trendify_db;
SOURCE database.sql;
```

---

### 3️⃣ Configure the Application

Edit `config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "trendify_db"
}

RAZORPAY_KEY_ID = "your_razorpay_key"
RAZORPAY_KEY_SECRET = "your_razorpay_secret"
```

---

### 4️⃣ Run the Application

```bash
python app1.py
```

Open in browser:
👉 http://127.0.0.1:5000

---

## 🔐 Admin Access

* URL: http://127.0.0.1:5000/admin/login
* Username: `admin`
* Password: `admin123`

---

## 📞 Contact

* **Email:** [support@trendify.com](mailto:support@trendify.com)
* **Phone:** +91 931366646

---

## 🔮 Future Enhancements

* Wishlist Feature
* Coupon & Discount System
* Advanced Filters (Price, Size, Brand)
* Mobile Responsive UI Improvements
* AI-Based Product Recommendations

---

## 👨‍💻 Author

**Pranjal Jotangiya**

---

## 📄 License

This project is open-source and available under the MIT License.
