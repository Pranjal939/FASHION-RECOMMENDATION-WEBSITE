# Trendify Deployment Guide

## 🚀 How to Deploy Your Application

### Step 1: Update Configuration

Open `config.py` and update the following:

```python
# For Local Development (Current Setup)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "trendify_db",
    "port": 3306
}

# For Production Deployment (Example)
DB_CONFIG = {
    "host": "your-database-server.com",  # Your database server IP or domain
    "user": "your_db_username",
    "password": "your_secure_password",
    "database": "trendify_db",
    "port": 3306
}
```

### Step 2: Change Flask Server Settings

```python
# For Local Development
FLASK_CONFIG = {
    "host": "127.0.0.1",  # Only accessible from your computer
    "port": 5000,
    "debug": True
}

# For Production
FLASK_CONFIG = {
    "host": "0.0.0.0",    # Accessible from network
    "port": 5000,
    "debug": False        # IMPORTANT: Set to False in production
}
```

### Step 3: Secure Your Application

1. **Change Secret Key:**
   ```python
   SECRET_KEY = "your-very-long-random-secret-key-here"
   ```

2. **Generate a secure secret key:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

### Step 4: Deployment Options

#### Option A: Deploy on Local Network
1. Set `host = "0.0.0.0"` in config.py
2. Run: `python app1.py`
3. Access from other devices: `http://YOUR_COMPUTER_IP:5000`
4. Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

#### Option B: Deploy on Cloud (Heroku, AWS, etc.)
1. Install production server: `pip install gunicorn` (Linux/Mac) or `pip install waitress` (Windows)
2. Create `requirements.txt`: `pip freeze > requirements.txt`
3. Use production WSGI server instead of Flask development server
4. Follow your cloud provider's deployment guide

#### Option C: Deploy with Waitress (Windows Production)
1. Install: `pip install waitress`
2. Create `run_production.py`:
   ```python
   from waitress import serve
   from app1 import app
   serve(app, host='0.0.0.0', port=5000)
   ```
3. Run: `python run_production.py`

### Step 5: Database Setup on Production

1. **Export your local database:**
   ```bash
   mysqldump -u root trendify_db > trendify_backup.sql
   ```

2. **Import to production database:**
   ```bash
   mysql -u your_user -p trendify_db < trendify_backup.sql
   ```

### Step 6: Security Checklist

- [ ] Changed SECRET_KEY to a random secure string
- [ ] Set debug=False in production
- [ ] Updated database credentials
- [ ] Set up firewall rules
- [ ] Use HTTPS (SSL certificate)
- [ ] Change default admin password
- [ ] Restrict database access
- [ ] Set up regular backups

### Step 7: Access Your Application

**Local Development:**
- Main Website: http://127.0.0.1:5000
- Admin Panel: http://127.0.0.1:5000/admin/login

**Network Access (after setting host to 0.0.0.0):**
- Main Website: http://YOUR_IP:5000
- Admin Panel: http://YOUR_IP:5000/admin/login

**Production Domain (after deployment):**
- Main Website: http://yourdomain.com
- Admin Panel: http://yourdomain.com/admin/login

## 🔧 Quick Configuration Changes

### To allow network access RIGHT NOW:

1. Open `config.py`
2. Change:
   ```python
   "host": "0.0.0.0",  # Change from "localhost" or "127.0.0.1"
   ```
3. Restart the Flask app
4. Access from other devices using your computer's IP address

### To find your computer's IP address:

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" (usually starts with 192.168.x.x)

**Mac/Linux:**
```bash
ifconfig
```
Look for "inet" address

## 📝 Notes

- Flask's built-in server is for development only
- For production, use a proper WSGI server (gunicorn, waitress, etc.)
- Always use HTTPS in production
- Keep your database credentials secure
- Regular backups are essential

## 🆘 Troubleshooting

**Can't access from other devices?**
- Check firewall settings
- Make sure host is set to "0.0.0.0"
- Verify you're using the correct IP address

**Database connection errors?**
- Verify database credentials in config.py
- Check if MySQL server is running
- Ensure database exists

**Port already in use?**
- Change port in config.py to something else (e.g., 8080)
- Or stop the process using that port
