import whois
import tldextract
import json

from urllib.parse import urlparse
from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def clean_value(value):

    if isinstance(value, list):

        if len(value) > 0:

            return value[0]

        return "Not Available"

    return value if value else "Not Available"


def format_date(value):

    try:

        return value.strftime(
            "%d %b %Y"
        )

    except:

        return str(value)


def whois_lookup(domain):

    # URL → domain
    if domain.startswith(("http://", "https://")):

        domain = urlparse(domain).netloc

    # Extract root domain
    extracted = tldextract.extract(domain)

    domain = extracted.domain + "." + extracted.suffix

    # Validation
    if "." not in domain:

        print("[red]Invalid domain name[/red]")

        return

    try:

        info = whois.whois(domain)

        registrar = str(
            clean_value(info.registrar)
        )

        creation = format_date(
            clean_value(info.creation_date)
        )

        expiration = format_date(
            clean_value(info.expiration_date)
        )

        organization = str(
            clean_value(info.org)
        )

        country = str(
            clean_value(info.country)
        )

        status = clean_value(info.status)

        if isinstance(status, list):

            status = ", ".join(
                list(set(status))
            )

        status = str(status)

        name_servers = info.name_servers

        # Clean duplicate nameservers
        if name_servers:

            if isinstance(
                name_servers,
                (list, set)
            ):

                cleaned_ns = sorted(
                    set(
                        ns.lower()
                        for ns in name_servers
                    )
                )

                ns_string = "\n".join(
                    cleaned_ns
                )

            else:

                ns_string = str(
                    name_servers
                ).lower()

        else:

            ns_string = "Not Available"

        # Create table
        table = Table(
            title=f"WHOIS Information - {domain}"
        )

        table.add_column(
            "Field",
            style="cyan",
            no_wrap=True
        )

        table.add_column(
            "Value",
            style="green"
        )

        table.add_row(
            "Domain",
            domain
        )

        table.add_row(
            "Registrar",
            registrar
        )

        table.add_row(
            "Created",
            creation
        )

        table.add_row(
            "Expires",
            expiration
        )

        table.add_row(
            "Organization",
            organization
        )

        table.add_row(
            "Country",
            country
        )

        table.add_row(
            "Status",
            status
        )

        table.add_row(
            "Name Servers",
            ns_string
        )

        console.print(table)

        # Save report
        report_data = {
            "domain": domain,
            "registrar": registrar,
            "creation_date": creation,
            "expiration_date": expiration,
            "organization": organization,
            "country": country,
            "status": status,
            "name_servers": (
                cleaned_ns
                if name_servers
                and isinstance(
                    name_servers,
                    (list, set)
                )
                else name_servers
            )
        }

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        report_file = (
            f"reports/"
            f"{domain}_whois_"
            f"{timestamp}.json"
        )

        with open(report_file, "w") as f:

            json.dump(
                report_data,
                f,
                indent=4
            )

        print(
            f"\n[bold green]"
            f"WHOIS report saved:"
            f"[/bold green] "
            f"{report_file}"
        )

    except Exception as e:

        print(
            f"[red]"
            f"WHOIS lookup failed:"
            f"[/red] {e}"
        )


def whois_menu():

    print(
        "\n[bold cyan]"
        "===== WHOIS LOOKUP ====="
        "[/bold cyan]"
    )

    while True:

        domain = console.input(
            "\n[bold green]"
            "toolkit/whois >[/bold green] "
        ).strip()

        if domain.lower() in [
            "back",
            "exit",
            "quit"
        ]:

            break

        whois_lookup(domain)

        print("\n1. Lookup Another Domain")
        print("2. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/whois >[/bold green] "
        ).strip()

        if choice == "2":

            break