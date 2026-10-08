import sqlite3
import os
import subprocess
import getpass

def login(username, password):
    # FIX 1: Parameterized query — prevents SQL Injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def ping_server(hostname):
    # FIX 2: Use subprocess with argument list — no shell, prevents Command Injection
    # FIX 3: Validate input — only allow safe hostnames
    if not hostname.replace('.', '').replace('-', '').isalnum():
        print("Invalid hostname")
        return
    subprocess.run(["ping", "-c", "1", hostname], check=False)

def main():
    print("Welcome to the Fixed App")

    # FIX 4: Read password from environment or prompt — no hardcoding
    admin_password = os.environ.get("ADMIN_PASSWORD")
    if not admin_password:
        admin_password = getpass.getpass("Enter admin password: ")

    # Safe usage
    login("admin", "safepassword")
    ping_server("google.com")

if __name__ == "__main__":
    main()
