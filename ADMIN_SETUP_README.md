# Trendify Admin Panel Setup Guide

## Issues Fixed

### Cart Page Issues:
1. ✅ Fixed duplicate `grand_total` calculation in cart.html
2. ✅ Removed redundant Jinja2 calculations (now handled by backend)
3. ✅ Cart now properly displays item totals and grand total

## Admin Panel Features

The admin panel includes:

- 📊 **Dashboard** - View statistics (total products, users, cart items)
- 📦 **Product Management** - Add, edit, delete products
- 👥 **User Management** - View all registered users
- 🔐 **Secure Login** - Password-protected admin access

## Setup Instructions

### Step 1: Create Admin Table and User

Run the setup script to create the admin table and default admin user:

```bash
python create_admin.py
```

This will:
- Create the `admins` table in your database
- Create a default admin user with credentials:
  - Username: `admin`
  - Password: `admin123`

### Step 2: Access Admin Panel

1. Start your Flask application:
   ```bash
   python app1.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:5000/admin/login
   ```

3. Login with:
   - Username: `admin`
   - Password: `admin123`

### Step 3: Change Default Password (Recommended)

For security, you should change the default password. You can create a new admin user by modifying `create_admin.py`:

```python
create_admin_user("yourusername", "yourpassword")
```

## Admin Panel URLs

- Login: `/admin/login`
- Dashboard: `/admin/dashboard`
- Products: `/admin/products`
- Add Product: `/admin/products/add`
- Edit Product: `/admin/products/edit/<id>`
- Users: `/admin/users`
- Logout: `/admin/logout`

## Features Overview

### Dashboard
- View total products count
- View total users count
- View total cart items
- Quick action buttons

### Product Management
- View all products in a table
- Add new products with all details
- Edit existing products
- Delete products (with confirmation)
- Upload images to `static/images/` folder

### User Management
- View all registered users
- See user IDs and usernames

## Security Features

- Password hashing using werkzeug.security
- Admin-only access with decorator
- Session-based authentication
- Logout functionality

## Notes

- Make sure your MySQL database is running
- Ensure the `trendify_db` database exists
- All product images should be placed in `static/images/` folder
- Admin panel is separate from the main website

## Troubleshooting

If you get a database error:
1. Check if MySQL is running
2. Verify database credentials in `app1.py`
3. Make sure `trendify_db` database exists

If admin login fails:
1. Run `create_admin.py` again
2. Check if the `admins` table exists
3. Verify credentials are correct

## Next Steps

You can customize the admin panel by:
- Adding more statistics to the dashboard
- Creating order management features
- Adding product categories management
- Implementing image upload functionality
- Adding search and filter options
