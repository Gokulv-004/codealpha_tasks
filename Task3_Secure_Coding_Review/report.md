# Secure Coding Review — Report

Author: Gokul V  
Student ID: CA/DF1/312305  
Date: October 2026  
Tool Used: Bandit (Python static security analyzer)  
Target: Custom Python app with intentional vulnerabilities

---

## Executive Summary

A static security review was performed on a sample Python application using
Bandit. Three security vulnerabilities were identified across severity
levels. All were remediated in the fixed version.

---

## Findings

### Finding 1: Command Injection (High Severity)

CWE: CWE-78  
Bandit Rule: B605 — start_process_with_a_shell  
Location: vulnerable_app/app.py:19

Vulnerable Code:
os.system("ping -c 1 " + hostname)

Risk:
An attacker can inject shell commands via the hostname parameter.
Example: hostname = "google.com; rm -rf /" would execute rm -rf /.

Remediation:
Use subprocess.run() with an argument list (no shell), and validate input:

if not hostname.replace('.', '').replace('-', '').isalnum():
    return
subprocess.run(["ping", "-c", "1", hostname], check=False)

Status: Fixed

---

### Finding 2: SQL Injection (Medium Severity)

CWE: CWE-89  
Bandit Rule: B608 — hardcoded_sql_expressions  
Location: vulnerable_app/app.py:11

Vulnerable Code:
query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)

Risk:
An attacker can bypass authentication with:
username = "admin' OR '1'='1"
password = "anything"

Remediation:
Use parameterized queries with placeholders:

query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))

Status: Fixed

---

### Finding 3: Hardcoded Password (Low Severity)

CWE: CWE-259  
Bandit Rule: B105 — hardcoded_password_string  
Location: vulnerable_app/app.py:5

Vulnerable Code:
ADMIN_PASSWORD = "supersecret123"

Risk:
Credentials in source code can be leaked via version control, logs,
or decompilation.

Remediation:
Use environment variables or a secrets manager:

admin_password = os.environ.get("ADMIN_PASSWORD")

Status: Fixed

---

## Summary Table

| # | Vulnerability | Severity | CWE | Status |
|---|---------------|----------|-----|--------|
| 1 | Command Injection | High | CWE-78 | Fixed |
| 2 | SQL Injection | Medium | CWE-89 | Fixed |
| 3 | Hardcoded Password | Low | CWE-259 | Fixed |

---

## Residual Warnings (Fixed App)

After remediation, Bandit reports only 3 Low-severity warnings related
to the subprocess module import and partial executable path. These
are acceptable because:

- subprocess is used safely (argument list, no shell)
- The absolute path is resolved at runtime by the OS
- Input validation prevents malicious hostnames

---

## Conclusion

Static analysis with Bandit successfully identified three real
vulnerabilities. All were remediated using industry best practices:

- Parameterized SQL queries
- Safe subprocess calls with input validation
- Environment-based secret management

Regular static analysis should be part of every development lifecycle.
