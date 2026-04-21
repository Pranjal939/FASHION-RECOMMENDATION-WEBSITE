import webbrowser
import time
import subprocess
import sys

print("=" * 50)
print("🔐 Starting Trendify Admin Panel")
print("=" * 50)

# Check if app is already running by trying to connect
import socket
def is_server_running(host='127.0.0.1', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

if not is_server_running():
    print("\n⚠️  Flask server is not running!")
    print("Starting Flask server...")
    
    # Start Flask app in background
    if sys.platform == "win32":
        subprocess.Popen(["python", "app1.py"], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(["python", "app1.py"])
    
    print("⏳ Waiting for server to start...")
    time.sleep(3)  # Wait for server to start
else:
    print("\n✅ Flask server is already running!")

# Open admin panel in browser
admin_url = "http://127.0.0.1:5000/admin/login"
print(f"\n🌐 Opening admin panel: {admin_url}")
print("\n📋 Admin Credentials:")
print("   Username: admin")
print("   Password: admin123")
print("\n" + "=" * 50)

webbrowser.open(admin_url)

print("\n✅ Admin panel opened in your browser!")
print("💡 Keep the Flask server running to use the admin panel.")
print("\n" + "=" * 50)
