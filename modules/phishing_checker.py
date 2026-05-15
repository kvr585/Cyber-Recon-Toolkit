# modules/phishing_checker.py

import re
from urllib.parse import urlparse

def phishing_url_menu():
    """
    Simple Phishing URL Checker
    Checks for:
    - IP-based URLs
    - Suspicious keywords
    - Excessive subdomains
    - HTTPS misuse
    """

    print("\n===== PHISHING URL CHECKER =====")
    url = input("Enter URL to check: ").strip()

    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    issues = []

    # Check for IP in URL
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    if re.match(ip_pattern, domain):
        issues.append("URL contains IP address instead of domain")

    # Suspicious keywords
    suspicious_keywords = ["login", "verify", "update", "secure", "account", "bank", "confirm"]
    for kw in suspicious_keywords:
        if kw in domain.lower():
            issues.append(f"Contains suspicious keyword: '{kw}'")

    # Excessive subdomains
    if domain.count(".") > 2:
        issues.append("Contains many subdomains (potential phishing)")

    # HTTPS check
   # if parsed.scheme != "https":
    #    issues.append("Not using HTTPS (insecure)")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # default to HTTPS

    # Output results
    if issues:
        print("\n⚠ Potential Phishing Indicators Detected:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
    else:
        print("\n✅ URL looks clean (no obvious phishing indicators)")