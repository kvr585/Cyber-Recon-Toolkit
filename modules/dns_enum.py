import dns.resolver
import json

from urllib.parse import urlparse

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def dns_lookup(domain):

    # Convert URL to domain
    if domain.startswith(("http://", "https://")):

        domain = urlparse(domain).netloc

    print(
        f"\n[bold yellow]"
        f"Target:[/bold yellow] {domain}"
    )

    record_types = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME"
    ]

    dns_results = {}

    for record in record_types:

        table = Table(
            title=f"{record} Records"
        )

        table.add_column(
            "Record Type",
            style="cyan"
        )

        table.add_column(
            "Value",
            style="green"
        )

        try:

            answers = dns.resolver.resolve(
                domain,
                record
            )

            dns_results[record] = []

            for answer in answers:

                value = answer.to_text()

                dns_results[record].append(value)

                table.add_row(
                    record,
                    value
                )

            console.print(table)

        except dns.resolver.NoAnswer:

            print(
                f"[yellow]"
                f"No {record} records found"
                f"[/yellow]"
            )

        except dns.resolver.NXDOMAIN:

            print(
                "[red]"
                "Domain does not exist"
                "[/red]"
            )

            return

        except dns.resolver.Timeout:

            print(
                "[red]"
                "DNS request timed out"
                "[/red]"
            )

        except Exception as e:

            print(
                f"[red]Error:[/red] {e}"
            )

    # Save report
    try:

        report_file = (
            f"reports/{domain}_dns.json"
        )

        with open(report_file, "w") as f:

            json.dump(
                dns_results,
                f,
                indent=4
            )

        print(
            f"\n[bold green]"
            f"DNS report saved:"
            f"[/bold green] "
            f"{report_file}"
        )

    except Exception as e:

        print(
            f"[red]"
            f"Failed to save report:"
            f"[/red] {e}"
        )


def dns_menu():

    print(
        "\n[bold cyan]"
        "===== DNS ENUMERATION ====="
        "[/bold cyan]"
    )

    while True:

        domain = console.input(
            "\n[bold green]"
            "toolkit/dns >[/bold green] "
        ).strip()

        if domain.lower() in [
            "back",
            "exit",
            "quit"
        ]:

            break

        dns_lookup(domain)

        print("\n1. Enumerate Another Domain")
        print("2. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/dns >[/bold green] "
        ).strip()

        if choice == "2":

            break