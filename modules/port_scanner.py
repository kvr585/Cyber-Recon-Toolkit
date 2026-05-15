import socket
import threading
import json
import ipaddress

from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()

scan_results = {}


def clean_banner(banner):

    try:

        return banner.split("\r\n")[0]

    except:

        return banner


def is_valid_target(target):

    # Domain validation
    if "." in target and not target.replace(".", "").isdigit():

        return True

    # IP validation
    try:

        ipaddress.ip_address(target)

        return True

    except:

        return False


def scan_port(target, port):

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        s.settimeout(1)

        result = s.connect_ex(
            (target, port)
        )

        if result == 0:

            try:

                service = socket.getservbyport(
                    port,
                    "tcp"
                )

            except:

                service = "Unknown"

            # Banner grabbing
            try:

                s.send(
                    b"HEAD / HTTP/1.0\r\n\r\n"
                )

                banner = s.recv(
                    1024
                ).decode(
                    errors="ignore"
                ).strip()

                banner = clean_banner(
                    banner
                )

            except:

                banner = "No Banner"

            # Example warning
            vulnerability = ""

            if "OpenSSH_6" in banner:

                vulnerability = (
                    "Potential outdated "
                    "OpenSSH version"
                )

            scan_results[port] = {
                "service": service,
                "banner": banner,
                "warning": vulnerability
            }

            print(
                f"[green][OPEN][/green] "
                f"Port {port} - {service}"
            )

            if banner != "No Banner":

                print(
                    f"[yellow]"
                    f"Banner:"
                    f"[/yellow] {banner}"
                )

            if vulnerability:

                print(
                    f"[red]"
                    f"Warning:"
                    f"[/red] {vulnerability}"
                )

            print()

        s.close()

    except:

        pass


def run_port_scan(
    target,
    start_port,
    end_port
):

    print(
        f"\n[bold green]"
        f"Scanning {target} "
        f"from port {start_port} "
        f"to {end_port}..."
        f"[/bold green]\n"
    )

    threads = []

    scan_results.clear()

    try:

        for port in range(
            start_port,
            end_port + 1
        ):

            t = threading.Thread(
                target=scan_port,
                args=(target, port)
            )

            threads.append(t)

            t.start()

        for t in threads:

            t.join()

        # Summary table
        if scan_results:

            table = Table(
                title="Open Ports Summary"
            )

            table.add_column(
                "Port",
                style="cyan"
            )

            table.add_column(
                "Service",
                style="green"
            )

            table.add_column(
                "Banner",
                style="yellow"
            )

            for port, details in scan_results.items():

                table.add_row(
                    str(port),
                    details["service"],
                    details["banner"]
                )

            console.print(table)

        else:

            print(
                "[yellow]"
                "No open ports found"
                "[/yellow]"
            )

        # Save report
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        report_file = (
            f"reports/"
            f"{target}_scan_"
            f"{timestamp}.json"
        )

        with open(report_file, "w") as f:

            json.dump(
                scan_results,
                f,
                indent=4
            )

        print(
            f"\n[bold green]"
            f"Scan Completed"
            f"[/bold green]\n"
            f"[bold cyan]"
            f"Report saved:"
            f"[/bold cyan] {report_file}"
        )

    except KeyboardInterrupt:

        print(
            "\n[red]"
            "Scan stopped by user"
            "[/red]"
        )

    except socket.gaierror:

        print(
            "[red]"
            "Hostname could not be resolved"
            "[/red]"
        )

    except socket.error:

        print(
            "[red]"
            "Connection error"
            "[/red]"
        )


def port_scan_menu():

    print(
        "\n[bold cyan]"
        "===== PORT SCANNER ====="
        "[/bold cyan]"
    )

    while True:

        target = console.input(
            "\n[bold green]"
            "toolkit/portscan >[/bold green] "
        ).strip()

        if target.lower() in [
            "back",
            "exit",
            "quit"
        ]:

            break

        if not is_valid_target(target):

            print(
                "[red]"
                "Invalid target."
                " Enter a valid IP or domain."
                "[/red]"
            )

            continue

        print(
            "\n[bold yellow]"
            "Select port range option:"
            "[/bold yellow]"
        )

        print("1. Common ports (1-1024)")
        print("2. All ports (1-65535)")
        print("3. Custom range")

        choice = console.input(
            "\n[bold green]"
            "toolkit/portscan >[/bold green] "
        ).strip()

        if choice == "1":

            start_port = 1
            end_port = 1024

        elif choice == "2":

            start_port = 1
            end_port = 65535

        elif choice == "3":

            start_port = int(
                console.input(
                    "\nStart Port > "
                )
            )

            end_port = int(
                console.input(
                    "End Port > "
                )
            )

        else:

            print(
                "[yellow]"
                "Invalid choice."
                " Using common ports"
                "[/yellow]"
            )

            start_port = 1
            end_port = 1024

        run_port_scan(
            target,
            start_port,
            end_port
        )

        print("\n1. Scan Another Target")
        print("2. Back to Main Menu")

        next_choice = console.input(
            "\n[bold green]"
            "toolkit/portscan >[/bold green] "
        ).strip()

        if next_choice == "2":

            break