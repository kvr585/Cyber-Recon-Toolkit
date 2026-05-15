import re
import os

def log_analyzer_menu():
    """
    Simple Log Analyzer
    Detects:
    - Failed login attempts
    - Repeated connections from same IP
    - Suspicious activity patterns
    """

    print("\n===== LOG ANALYZER =====")

    log_file = input("Enter path to log file (e.g., /var/log/auth.log): ").strip()

    if not os.path.exists(log_file):
        print("File does not exist.")
        return

    try:
        with open(log_file, "r") as f:
            logs = f.readlines()

        failed_login_pattern = re.compile(r"Failed password|authentication failure", re.IGNORECASE)
        ip_pattern = re.compile(r"(\d{1,3}\.){3}\d{1,3}")

        failed_attempts = {}
        total_failed = 0

        for line in logs:
            if failed_login_pattern.search(line):
                total_failed += 1
                ip_match = ip_pattern.search(line)
                if ip_match:
                    ip = ip_match.group()
                    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

        print(f"\nTotal failed login attempts detected: {total_failed}\n")

        if failed_attempts:
            print("Top suspicious IPs by failed attempts:")
            sorted_ips = sorted(failed_attempts.items(), key=lambda x: x[1], reverse=True)
            for ip, count in sorted_ips[:10]:
                print(f"{ip}: {count} failed attempts")
        else:
            print("No suspicious IPs detected.")

    except Exception as e:
        print(f"Error reading log file: {e}")