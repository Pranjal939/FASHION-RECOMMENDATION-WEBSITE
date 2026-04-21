from werkzeug.security import generate_password_hash

# Generate hash for 'admin123'
password = 'admin123'
hashed = generate_password_hash(password)

print("=" * 60)
print("ADMIN PASSWORD HASH GENERATOR")
print("=" * 60)
print(f"\nPlain Password: {password}")
print(f"\nHashed Password:\n{hashed}")
print("\n" + "=" * 60)
print("\nUse this SQL command:")
print("=" * 60)
print(f"""
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO admins (username, password) 
VALUES ('admin', '{hashed}');
""")
print("=" * 60)
