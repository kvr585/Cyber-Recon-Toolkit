import re

from urllib.parse import urlparse

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def analyze_url(url):

    suspicious_keywords = [
        "login",
        "verify",
        "update",
        "secure",
        "account",
        "bank",
        "confirm"
    ]

    print(
        f"\n[bold yellow]"
        f"Checking URL:"
        f"[/bold yellow] {url}"
    )

    if not url.startswith(
        ("http://", "https://")
    ):

        url = "https://" + url

    parsed = urlparse(url)

    domain = parsed.netloc

    issues = []

    # IP address detection
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, domain):

        issues.append(
            "URL contains IP address instead of domain"
        )

    # Suspicious keywords
    for kw in suspicious_keywords:

        if kw in domain.lower():

            issues.append(
                f"Contains suspicious keyword: '{kw}'"
            )

    # Excessive subdomains
    if domain.count(".") > 2:

        issues.append(
            "Contains many subdomains "
            "(potential phishing)"
        )

    # HTTPS check
    if parsed.scheme != "https":

        issues.append("Not using HTTPS")

    # Output
    if issues:

        table = Table(
            title="⚠ Potential Phishing Indicators"
        )

        table.add_column(
            "Issue",
            style="red"
        )

        for issue in issues:

            table.add_row(issue)

        console.print(table)

    else:

        print(
            "[green]"
            "✅ URL looks clean "
            "(no obvious phishing indicators)"
            "[/green]"
        )


def phishing_url_menu():

    while True:

        print(
            "\n[bold cyan]"
            "===== PHISHING URL CHECKER ====="
            "[/bold cyan]"
        )

        print("\n1. Check Single URL")
        print("2. Batch URL Scan")
        print("3. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/phishing >[/bold green] "
        ).strip()

        if choice == "1":

            url = console.input(
                "\nURL > "
            ).strip()

            analyze_url(url)

        elif choice == "2":

            file_path = console.input(
                "\nFile Path > "
            ).strip()

            try:

                with open(file_path, "r") as f:

                    urls = [
                        line.strip()
                        for line in f
                        if line.strip()
                    ]

                for url in urls:

                    analyze_url(url)

            except Exception as e:

                print(
                    f"[red]"
                    f"Failed to read file:"
                    f"[/red] {e}"
                )

        elif choice == "3":

            break

        else:

            print("[red]Invalid choice[/red]")