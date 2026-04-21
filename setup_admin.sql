-- Create admins table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin (username: admin, password: admin123)
-- Password is hashed using werkzeug.security
INSERT INTO admins (username, password) VALUES 
('admin', 'scrypt:32768:8:1$YourSaltHere$hashedpassword');

-- Note: You need to run this Python code to generate the proper password hash:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))
-- Then replace the password value above with the generated hash
