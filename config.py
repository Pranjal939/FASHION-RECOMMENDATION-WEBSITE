# Trendify Configuration File

# ================= DATABASE CONFIGURATION =================
# Change these values to match your production database
DB_CONFIG = {
    "host": "localhost",  # Change to your database server IP or domain
    "user": "root",       # Change to your database username
    "password": "",       # Change to your database password
    "database": "trendify_db",
    "port": 3306
}

# ================= FLASK SERVER CONFIGURATION =================
# Change these values for production deployment
FLASK_CONFIG = {
    "host": "0.0.0.0",    # 0.0.0.0 allows external access, 127.0.0.1 for local only
    "port": 5000,         # Change port if needed
    "debug": True         # Set to False in production
}

# ================= APPLICATION CONFIGURATION =================
SECRET_KEY = "trendify_secret_key_123"  # Change this in production!

# ================= RAZORPAY CONFIGURATION =================
RAZORPAY_KEY_ID = "rzp_test_SZijrkHNdlco2x"
RAZORPAY_KEY_SECRET = "28WO2jZlG3QJESSkhKeIF913"
# For production deployment:
# 1. Change DB_CONFIG host to your database server
# 2. Set FLASK_CONFIG debug to False
# 3. Change SECRET_KEY to a random secure string
# 4. Use a production WSGI server (gunicorn, waitress, etc.)
# 5. Set up proper firewall and security rules
