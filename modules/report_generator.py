import os
import json
import csv

from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def generate_combined_report():

    report_data = {}

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    report_data["report_generated"] = (
        timestamp
    )

    reports_folder = "reports"

    if not os.path.exists(reports_folder):

        os.makedirs(reports_folder)

    report_files = [
        f for f in os.listdir(reports_folder)
        if f.endswith(".json")
    ]

    if not report_files:

        print(
            "[yellow]"
            "No module reports found "
            "in reports folder."
            "[/yellow]"
        )

        return

    report_data["module_reports"] = {}

    print(
        "\n[bold yellow]"
        "Collecting module reports..."
        "[/bold yellow]"
    )

    for file in report_files:

        try:

            with open(
                os.path.join(
                    reports_folder,
                    file
                ),
                "r"
            ) as f:

                module_name = file.replace(
                    ".json",
                    ""
                )

                report_data[
                    "module_reports"
                ][module_name] = json.load(f)

        except Exception as e:

            print(
                f"[red]"
                f"Failed to read {file}:"
                f"[/red] {e}"
            )

    # Summary table
    table = Table(
        title="Loaded Reports Summary"
    )

    table.add_column(
        "Report File",
        style="cyan"
    )

    table.add_column(
        "Status",
        style="green"
    )

    for file in report_files:

        table.add_row(
            file,
            "Loaded"
        )

    console.print(table)

    # Save combined JSON
    combined_json_file = (
        f"{reports_folder}/"
        f"combined_report_"
        f"{timestamp}.json"
    )

    try:

        with open(
            combined_json_file,
            "w"
        ) as f:

            json.dump(
                report_data,
                f,
                indent=4
            )

        print(
            f"\n[bold green]"
            f"Combined JSON report saved:"
            f"[/bold green] "
            f"{combined_json_file}"
        )

    except Exception as e:

        print(
            f"[red]"
            f"Error saving JSON report:"
            f"[/red] {e}"
        )

    # Save combined CSV
    combined_csv_file = (
        f"{reports_folder}/"
        f"combined_report_"
        f"{timestamp}.csv"
    )

    try:

        with open(
            combined_csv_file,
            "w",
            newline=""
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow([
                "Module",
                "Target",
                "Key",
                "Data"
            ])

            for module, content in (
                report_data[
                    "module_reports"
                ].items()
            ):

                if isinstance(content, dict):

                    for key, value in content.items():

                        writer.writerow([
                            module,
                            key,
                            "",
                            json.dumps(value)
                        ])

                else:

                    writer.writerow([
                        module,
                        "",
                        "",
                        json.dumps(content)
                    ])

        print(
            f"[bold green]"
            f"Combined CSV report saved:"
            f"[/bold green] "
            f"{combined_csv_file}"
        )

    except Exception as e:

        print(
            f"[red]"
            f"Error saving CSV report:"
            f"[/red] {e}"
        )


def generate_report_menu():

    print(
        "\n[bold cyan]"
        "===== REPORT GENERATOR ====="
        "[/bold cyan]"
    )

    while True:

        print("\n1. Generate Combined Report")
        print("2. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/reports >[/bold green] "
        ).strip()

        if choice == "1":

            generate_combined_report()

        elif choice == "2":

            break

        else:

            print("[red]Invalid choice[/red]")