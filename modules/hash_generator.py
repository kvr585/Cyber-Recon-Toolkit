import hashlib
import os

from rich import print
from rich.console import Console


console = Console()


def generate_hash(data):

    md5_hash = hashlib.md5(data).hexdigest()

    sha1_hash = hashlib.sha1(data).hexdigest()

    sha256_hash = hashlib.sha256(data).hexdigest()

    sha512_hash = hashlib.sha512(data).hexdigest()

    print(f"\n[green]MD5:[/green] {md5_hash}")

    print(f"[green]SHA1:[/green] {sha1_hash}")

    print(f"[green]SHA256:[/green] {sha256_hash}")

    print(f"[green]SHA512:[/green] {sha512_hash}")


def hash_menu():

    while True:

        print(
            "\n[bold cyan]"
            "===== HASH GENERATOR ====="
            "[/bold cyan]"
        )

        print("\n1. Hash Text")
        print("2. Hash File")
        print("3. Back to Main Menu")

        choice = console.input(
            "\n[bold green]"
            "toolkit/hash >[/bold green] "
        ).strip()

        if choice == "1":

            text = console.input(
                "\nText > "
            )

            generate_hash(text.encode())

        elif choice == "2":

            file_path = console.input(
                "\nFile Path > "
            )

            if not os.path.exists(file_path):

                print(
                    f"[red]"
                    f"File does not exist:"
                    f"[/red] {file_path}"
                )

                continue

            try:

                with open(file_path, "rb") as f:

                    data = f.read()

                generate_hash(data)

            except Exception as e:

                print(
                    f"[red]"
                    f"Error reading file:"
                    f"[/red] {e}"
                )

        elif choice == "3":

            break

        else:

            print("[red]Invalid choice[/red]")