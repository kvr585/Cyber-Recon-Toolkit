import hashlib
import os
import json

from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()


def format_size(size):

    for unit in ["B", "KB", "MB", "GB"]:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


def calculate_hashes_from_data(data):

    hashes = {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "sha512": hashlib.sha512(data).hexdigest()
    }

    return hashes


def calculate_file_hashes(file_path):

    md5 = hashlib.md5()

    sha1 = hashlib.sha1()

    sha256 = hashlib.sha256()

    sha512 = hashlib.sha512()

    with open(file_path, "rb") as f:

        while chunk := f.read(4096):

            md5.update(chunk)

            sha1.update(chunk)

            sha256.update(chunk)

            sha512.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest(),
        "sha512": sha512.hexdigest()
    }


def display_hashes(hashes):

    table = Table(
        title="Generated Hashes"
    )

    table.add_column(
        "Algorithm",
        style="cyan"
    )

    table.add_column(
        "Hash",
        style="green"
    )

    table.add_row(
        "MD5",
        hashes["md5"]
    )

    table.add_row(
        "SHA1",
        hashes["sha1"]
    )

    table.add_row(
        "SHA256",
        hashes["sha256"]
    )

    table.add_row(
        "SHA512",
        hashes["sha512"]
    )

    console.print(table)


def save_hash_report(report_data):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    report_file = (
        f"reports/"
        f"hash_report_{timestamp}.json"
    )

    try:

        with open(report_file, "w") as f:

            json.dump(
                report_data,
                f,
                indent=4
            )

        print(
            f"\n[bold green]"
            f"Hash report saved:"
            f"[/bold green] "
            f"{report_file}"
        )

    except Exception as e:

        print(
            f"[red]"
            f"Failed to save report:"
            f"[/red] {e}"
        )


def verify_hash(file_path, expected_hash):

    try:

        hashes = calculate_file_hashes(
            file_path
        )

        matched = False

        for algorithm, value in hashes.items():

            if value.lower() == expected_hash.lower():

                print(
                    f"\n[bold green]"
                    f"Hash verified "
                    f"({algorithm.upper()})"
                    f"[/bold green]"
                )

                matched = True

                break

        if not matched:

            print(
                "\n[bold red]"
                "Hash mismatch detected"
                "[/bold red]"
            )

    except Exception as e:

        print(
            f"[red]"
            f"Verification failed:"
            f"[/red] {e}"
        )


def hash_menu():

    while True:

        print(
            "\n[bold cyan]"
            "===== HASH GENERATOR ====="
            "[/bold cyan]"
        )

        print("\n1. Hash Text")
        print("2. Hash File")
        print("3. Verify File Hash")
        print("4. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/hash >[/bold green] "
        ).strip()

        # HASH TEXT
        if choice == "1":

            text = console.input(
                "\nText > "
            )

            hashes = calculate_hashes_from_data(
                text.encode()
            )

            display_hashes(hashes)

            report_data = {
                "type": "text",
                "input": text,
                "hashes": hashes
            }

            save_hash_report(report_data)

        # HASH FILE
        elif choice == "2":

            file_path = console.input(
                "\nFile Path > "
            ).strip()

            if not os.path.exists(file_path):

                print(
                    f"[red]"
                    f"File does not exist:"
                    f"[/red] {file_path}"
                )

                continue

            try:

                file_size = os.path.getsize(
                    file_path
                )

                formatted_size = format_size(
                    file_size
                )

                print(
                    f"\n[bold yellow]"
                    f"File Size:"
                    f"[/bold yellow] "
                    f"{formatted_size}"
                )

                hashes = calculate_file_hashes(
                    file_path
                )

                display_hashes(hashes)

                report_data = {
                    "type": "file",
                    "file_path": file_path,
                    "file_size": formatted_size,
                    "hashes": hashes
                }

                save_hash_report(report_data)

            except Exception as e:

                print(
                    f"[red]"
                    f"Error reading file:"
                    f"[/red] {e}"
                )

        # VERIFY HASH
        elif choice == "3":

            file_path = console.input(
                "\nFile Path > "
            ).strip()

            if not os.path.exists(file_path):

                print(
                    f"[red]"
                    f"File does not exist:"
                    f"[/red] {file_path}"
                )

                continue

            expected_hash = console.input(
                "Expected Hash > "
            ).strip()

            verify_hash(
                file_path,
                expected_hash
            )

        # BACK
        elif choice == "4":

            break

        else:

            print("[red]Invalid choice[/red]")