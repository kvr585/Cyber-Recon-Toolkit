import subprocess
import threading
import json

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


def run_ping_sweep(subnet):

    # Validate subnet
    parts = subnet.split(".")

    if len(parts) != 3:

        print(
            "[red]"
            "Invalid subnet."
            " Format should be like 192.168.1"
            "[/red]"
        )

        return

    threads = []

    alive_hosts.clear()

    print(
        f"\n[bold yellow]"
        f"Scanning subnet:"
        f"[/bold yellow] {subnet}.0/24\n"
    )

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

    print(
        "\n[bold yellow]"
        "Ping Sweep Completed"
        "[/bold yellow]"
    )

    if alive_hosts:

        print(
            f"\n[bold green]"
            f"Alive Hosts ({len(alive_hosts)}):"
            f"[/bold green]"
        )

        for host in alive_hosts:

            print(f"- {host}")

        # Save report
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
            "toolkit/pingsweep >[/bold green] "
        ).strip()

        if subnet.lower() in [
            "back",
            "exit",
            "quit"
        ]:

            break

        run_ping_sweep(subnet)

        print("\n1. Scan Another Subnet")
        print("2. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/pingsweep >[/bold green] "
        ).strip()

        if choice == "2":

            break