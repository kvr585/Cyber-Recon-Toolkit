import subprocess
import threading
import json
import time

from datetime import datetime

from rich import print
from rich.console import Console


console = Console()

alive_hosts = []


def ping_host(ip):

    try:

        subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", ip],
            stderr=subprocess.DEVNULL
        )

        alive_hosts.append(ip)

        print(
            f"[green][ALIVE][/green] {ip}"
        )

    except:

        pass


def validate_subnet(subnet):

    parts = subnet.split(".")

    if len(parts) != 3:

        return False

    try:

        for part in parts:

            value = int(part)

            if value < 0 or value > 255:

                return False

        return True

    except:

        return False


def sort_ips(ip_list):

    return sorted(
        ip_list,
        key=lambda ip: list(
            map(int, ip.split("."))
        )
    )


def save_report():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    report_file = (
        f"reports/"
        f"ping_sweep_{timestamp}.json"
    )

    try:

        with open(report_file, "w") as f:

            json.dump(
                alive_hosts,
                f,
                indent=4
            )

        print(
            f"\n[bold green]"
            f"Report saved:"
            f"[/bold green] "
            f"{report_file}"
        )

    except Exception as e:

        print(
            f"[red]"
            f"Failed to save report:"
            f"[/red] {e}"
        )


def run_ping_sweep(subnet):

    threads = []

    alive_hosts.clear()

    print(
        f"\n[bold yellow]"
        f"Scanning subnet:"
        f"[/bold yellow] {subnet}.0/24\n"
    )

    start_time = time.time()

    for i in range(1, 255):

        ip = f"{subnet}.{i}"

        t = threading.Thread(
            target=ping_host,
            args=(ip,)
        )

        threads.append(t)

        t.start()

    for t in threads:

        t.join()

    end_time = time.time()

    elapsed = round(
        end_time - start_time,
        2
    )

    print(
        "\n[bold yellow]"
        "Ping Sweep Completed"
        "[/bold yellow]"
    )

    print(
        f"[bold cyan]"
        f"Scan completed in "
        f"{elapsed} seconds"
        f"[/bold cyan]"
    )

    if alive_hosts:

        sorted_hosts = sort_ips(
            alive_hosts
        )

        print(
            f"\n[bold green]"
            f"Alive Hosts Found:"
            f" {len(sorted_hosts)}"
            f"[/bold green]"
        )

        for host in sorted_hosts:

            print(f"- {host}")

        alive_hosts.clear()

        alive_hosts.extend(sorted_hosts)

        save_report()

    else:

        print(
            "[yellow]"
            "No alive hosts detected"
            "[/yellow]"
        )


def ping_sweep_menu():

    print(
        "\n[bold cyan]"
        "===== PING SWEEP ====="
        "[/bold cyan]"
    )

    while True:

        subnet = console.input(
            "\n[bold green]"
            "Subnet >[/bold green] "
        ).strip()

        if subnet.lower() in [
            "back",
            "exit",
            "quit"
        ]:

            break

        if not validate_subnet(subnet):

            print(
                "[red]"
                "Invalid subnet format."
                " Example: 192.168.1"
                "[/red]"
            )

            continue

        run_ping_sweep(subnet)

        print("\n1. Scan Another Subnet")
        print("2. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "Choice >[/bold green] "
        ).strip()

        if choice == "2":

            break