import dns.resolver
import json
import time

from urllib.parse import urlparse

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def truncate_value(value, limit=80):

    if len(value) > limit:

        return value[:limit] + "..."

    return value


def dns_lookup(domain):

    # Convert URL to domain
    if domain.startswith(("http://", "https://")):

        domain = urlparse(domain).netloc

    print(
        f"\n[bold yellow]"
        f"Target:[/bold yellow] {domain}"
    )

    start_time = time.time()

    record_types = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME"
    ]

    dns_results = {}

    # Single unified table
    table = Table(
        title=f"DNS Enumeration - {domain}"
    )

    table.add_column(
        "Type",
        style="cyan",
        no_wrap=True
    )

    table.add_column(
        "Value",
        style="green"
    )

    for record in record_types:

        try:

            answers = dns.resolver.resolve(
                domain,
                record
            )

            dns_results[record] = []

            for answer in answers:

                value = answer.to_text()

                dns_results[record].append(value)

                display_value = truncate_value(
                    value
                )

                table.add_row(
                    record,
                    display_value
                )

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
                f"[red]"
                f"Error resolving "
                f"{record}:"
                f"[/red] {e}"
            )

    console.print(table)

    # DNS Summary
    print(
        "\n[bold cyan]"
        "DNS Summary"
        "[/bold cyan]"
    )

    for record, values in dns_results.items():

        print(
            f"[green]{record}[/green]: "
            f"{len(values)} records"
        )

    # Timing
    end_time = time.time()

    elapsed = round(
        end_time - start_time,
        2
    )

    print(
        f"\n[bold yellow]"
        f"Enumeration completed in "
        f"{elapsed} seconds"
        f"[/bold yellow]"
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