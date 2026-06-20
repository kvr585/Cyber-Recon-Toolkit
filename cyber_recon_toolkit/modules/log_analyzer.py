import re
import os
import json

from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def analyze_log(log_file):

    try:

        with open(log_file, "r") as f:

            logs = f.readlines()

        failed_login_pattern = re.compile(
            r"Failed password|authentication failure",
            re.IGNORECASE
        )

        ip_pattern = re.compile(
            r"(\d{1,3}\.){3}\d{1,3}"
        )

        failed_attempts = {}

        total_failed = 0

        for line in logs:

            if failed_login_pattern.search(line):

                total_failed += 1

                ip_match = ip_pattern.search(line)

                if ip_match:

                    ip = ip_match.group()

                    failed_attempts[ip] = (
                        failed_attempts.get(ip, 0) + 1
                    )

        print(
            f"\n[bold yellow]"
            f"Total failed login attempts detected:"
            f"[/bold yellow] {total_failed}\n"
        )

        if failed_attempts:

            table = Table(
                title="Top Suspicious IPs"
            )

            table.add_column(
                "IP Address",
                style="cyan"
            )

            table.add_column(
                "Failed Attempts",
                style="red"
            )

            sorted_ips = sorted(
                failed_attempts.items(),
                key=lambda x: x[1],
                reverse=True
            )

            for ip, count in sorted_ips[:10]:

                table.add_row(
                    ip,
                    str(count)
                )

            console.print(table)

            # Save report
            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            report_file = (
                f"reports/"
                f"log_summary_{timestamp}.json"
            )

            summary = {
                "log_file": log_file,
                "total_failed_attempts": total_failed,
                "top_ips": sorted_ips[:10]
            }

            with open(report_file, "w") as f:

                json.dump(
                    summary,
                    f,
                    indent=4
                )

            print(
                f"\n[bold green]"
                f"Summary JSON saved:"
                f"[/bold green] "
                f"{report_file}"
            )

        else:

            print(
                "[green]"
                "No suspicious IPs detected."
                "[/green]"
            )

    except Exception as e:

        print(
            f"[red]"
            f"Error reading log file:"
            f"[/red] {e}"
        )


def log_analyzer_menu():

    print(
        "\n[bold cyan]"
        "===== LOG ANALYZER ====="
        "[/bold cyan]"
    )

    print(
        "\n[dim]"
        "Examples:"
        "\n/var/log/auth.log"
        "\n/var/log/syslog"
        "\n/var/log/apache2/access.log"
        "[/dim]"
    )

    while True:

        log_file = console.input(
            "\n[bold green]"
            "toolkit/logs >[/bold green] "
        ).strip()

        if log_file.lower() in [
            "back",
            "exit",
            "quit"
        ]:

            break

        if not os.path.exists(log_file):

            print(
                f"[red]"
                f"File does not exist:"
                f"[/red] {log_file}"
            )

            continue

        analyze_log(log_file)

        print("\n1. Analyze Another Log File")
        print("2. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/logs >[/bold green] "
        ).strip()

        if choice == "2":

            break