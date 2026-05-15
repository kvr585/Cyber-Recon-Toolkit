from rich import print
from rich.console import Console
from rich.panel import Panel

from modules.hash_generator import hash_menu
from modules.whois_lookup import whois_menu
from modules.dns_enum import dns_menu
from modules.port_scanner import port_scan_menu
from modules.ping_sweep import ping_sweep_menu
from modules.phishing_checker import phishing_url_menu
from modules.log_analyzer import log_analyzer_menu
from modules.report_generator import generate_report_menu


console = Console()


def display_banner():

    banner = """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝

████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
   ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
   ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
   ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
"""

    console.print(
        Panel.fit(
            banner,
            title="[bold cyan]Cyber Recon Toolkit[/bold cyan]",
            border_style="green"
        )
    )


def display_menu():

    menu = """
[bold cyan]RECON[/bold cyan]
[cyan]1.[/cyan] WHOIS Lookup
[cyan]2.[/cyan] DNS Enumeration
[cyan]3.[/cyan] Ping Sweep

[bold yellow]SCANNING[/bold yellow]
[cyan]4.[/cyan] Port Scanner
[cyan]5.[/cyan] Log Analyzer

[bold magenta]UTILITIES[/bold magenta]
[cyan]6.[/cyan] Hash Generator
[cyan]7.[/cyan] Phishing URL Checker
[cyan]8.[/cyan] Generate Combined Report

[bold red]SYSTEM[/bold red]
[red]9.[/red] Exit
"""

    console.print(
        Panel(
            menu,
            title="[bold green]MAIN MENU[/bold green]",
            border_style="cyan",
            expand=False,
            padding=(0, 2)
        )
    )


def main():

    display_banner()

    while True:

        display_menu()

        choice = console.input(
            "\n[bold green]toolkit >[/bold green] "
        ).strip()

        if choice == "1":

            whois_menu()

        elif choice == "2":

            dns_menu()

        elif choice == "3":

            ping_sweep_menu()

        elif choice == "4":

            port_scan_menu()

        elif choice == "5":

            log_analyzer_menu()

        elif choice == "6":

            hash_menu()

        elif choice == "7":

            phishing_url_menu()

        elif choice == "8":

            generate_report_menu()

        elif choice == "9":

            print(
                "\n[bold red]"
                "Exiting Cyber Toolkit..."
                "[/bold red]"
            )

            break

        else:

            print(
                "[red]"
                "Invalid choice. Try again."
                "[/red]"
            )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n[bold red]"
            "Toolkit interrupted by user."
            "[/bold red]"
        )

        print(
            "[bold yellow]"
            "Exiting gracefully..."
            "[/bold yellow]"
        )