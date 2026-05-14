import socket
import threading
import json
from colorama import Fore, Style


scan_results = {}


def scan_port(target, port):

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:

            try:
                service = socket.getservbyport(port)

            except:
                service = "Unknown"

            # Banner grabbing
            try:

                s.send(b"HEAD / HTTP/1.0\r\n\r\n")

                banner = s.recv(1024).decode().strip()

            except:
                banner = "No Banner"

            # Save results
            scan_results[port] = {
                "service": service,
                "banner": banner
            }

            # Print results
            print(
                Fore.GREEN +
                f"[OPEN] Port {port} - {service}" +
                Style.RESET_ALL
            )

            if banner != "No Banner":
                print(f"Banner: {banner}\n")

        s.close()

    except:
        pass


def port_scan_menu():

    print("\n===== PORT SCANNER =====")

    target = input("Enter target IP or domain: ").strip()

    print("\nSelect port range option:")
    print("1. Common ports (1-1024)")
    print("2. All ports (1-65535)")
    print("3. Custom range")

    choice = input("Enter choice: ").strip()

    if choice == "1":

        start_port = 1
        end_port = 1024

    elif choice == "2":

        start_port = 1
        end_port = 65535

    elif choice == "3":

        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))

    else:

        print("Invalid choice, using common ports")

        start_port = 1
        end_port = 1024

    print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

    threads = []

    try:

        for port in range(start_port, end_port + 1):

            t = threading.Thread(
                target=scan_port,
                args=(target, port)
            )

            threads.append(t)

            t.start()

        for t in threads:
            t.join()

        # Save JSON report
        report_file = f"reports/{target}_scan.json"

        with open(report_file, "w") as f:
            json.dump(scan_results, f, indent=4)

        print(
            Fore.CYAN +
            f"\nScan Completed. Report saved to {report_file}" +
            Style.RESET_ALL
        )

    except KeyboardInterrupt:
        print("\nScan stopped by user")

    except socket.gaierror:
        print("Hostname could not be resolved")

    except socket.error:
        print("Connection error")