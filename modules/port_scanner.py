import socket
import json
import ipaddress
import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

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


def resolve_target(target):

    try:

        resolved_ip = socket.gethostbyname(
            target
        )

        print(
            f"[cyan]"
            f"Resolved IP:"
            f"[/cyan] {resolved_ip}"
        )

        return resolved_ip

    except:

        return None


def get_banner(socket_obj, port):

    http_ports = [
        80,
        8000,
        8080
    ]

    if port not in http_ports:

        return "No Banner"

    try:

        socket_obj.send(
            b"HEAD / HTTP/1.0\r\n\r\n"
        )

        banner = socket_obj.recv(
            1024
        ).decode(
            errors="ignore"
        ).strip()

        banner = clean_banner(
            banner
        )

        if banner:

            return banner

        return "No Banner"

    except:

        return "No Banner"


def scan_port(target, port):

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        s.settimeout(0.3)

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

            banner = get_banner(
                s,
                port
            )

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
                f"\n[green][OPEN][/green] "
                f"Port {port} - {service}"
            )

            if (
                banner and
                banner != "No Banner"
            ):

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

        s.close()

    except:

        pass


def save_report(target):

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
        f"\n[bold cyan]"
        f"Report saved:"
        f"[/bold cyan] {report_file}"
    )


def display_summary():

    if scan_results:

        table = Table(
            title=(
                f"Open Ports Summary "
                f"({len(scan_results)} Open)"
            )
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

        for port in sorted(scan_results):

            details = scan_results[port]

            banner_display = (
                details["banner"]
                if details["banner"] != "No Banner"
                else "-"
            )

            table.add_row(
                str(port),
                details["service"],
                banner_display
            )

        console.print(table)

        print(
            f"[bold green]"
            f"Open ports found:"
            f"[/bold green] "
            f"{len(scan_results)}"
        )

    else:

        print(
            "[yellow]"
            "Scan finished."
            " No open ports detected "
            "in selected range."
            "[/yellow]"
        )


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

    resolved_ip = resolve_target(
        target
    )

    if not resolved_ip:

        print(
            "[red]"
            "Failed to resolve target."
            "[/red]"
        )

        return

    scan_results.clear()

    start_time = time.time()

    futures = []

    try:

        with ThreadPoolExecutor(
            max_workers=50
        ) as executor:

            for port in range(
                start_port,
                end_port + 1
            ):

                future = executor.submit(
                    scan_port,
                    resolved_ip,
                    port
                )

                futures.append(future)

                if (
                    port % 5000 == 0 and
                    port != end_port
                ):

                    print(
                        f"[cyan]"
                        f"Scanned {port} ports..."
                        f"[/cyan]"
                    )

            for future in as_completed(
                futures
            ):

                future.result()

        if end_port > 5000:

            print(
                "\n[cyan]"
                "Finalizing scan results..."
                "[/cyan]"
            )

        end_time = time.time()

        elapsed = round(
            end_time - start_time,
            2
        )

        display_summary()

        print(
            f"\n[bold green]"
            f"Scan Completed"
            f"[/bold green]"
        )

        print(
            f"[bold cyan]"
            f"Scan completed in "
            f"{elapsed} seconds"
            f"[/bold cyan]"
        )

        save_report(target)

    except KeyboardInterrupt:

        print(
            "\n[red]"
            "Scan interrupted by user."
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
            "Target >[/bold green] "
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
        print("2. Extended scan (1-10000)")
        print("3. Custom range")

        choice = console.input(
            "\n[bold green]"
            "Choice >[/bold green] "
        ).strip()

        if choice == "1":

            start_port = 1
            end_port = 1024

        elif choice == "2":

            start_port = 1
            end_port = 10000

        elif choice == "3":

            try:

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

                if (
                    start_port < 1 or
                    end_port > 65535
                ):

                    print(
                        "[red]"
                        "Ports must be between "
                        "1 and 65535"
                        "[/red]"
                    )

                    continue

                if start_port > end_port:

                    print(
                        "[red]"
                        "Start port cannot be "
                        "greater than end port"
                        "[/red]"
                    )

                    continue

            except:

                print(
                    "[red]"
                    "Invalid port range"
                    "[/red]"
                )

                continue

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
            "Choice >[/bold green] "
        ).strip()

        if next_choice == "2":

            break