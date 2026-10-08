import sqlite3
import os

# VULNERABILITY 1: Hardcoded credentials
ADMIN_PASSWORD = "supersecret123"

def login(username, password):
    # VULNERABILITY 2: SQL Injection (string formatting in SQL query)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def ping_server(hostname):
    # VULNERABILITY 3: Command Injection (unsafe os.system)
    os.system("ping -c 1 " + hostname)

def main():
    print("Welcome to the Vulnerable App")
    # Simulating a login with SQL injection payload
    login("admin", "' OR '1'='1")
    # Simulating command injection
    ping_server("google.com; ls -la")

if __name__ == "__main__":
    main()
