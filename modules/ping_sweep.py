import subprocess
import threading

def ping_host(ip):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", ip],
            stderr=subprocess.DEVNULL
        )
        print(f"[ALIVE] {ip}")
    except: 
        pass

def ping_sweep_menu():
    print("\n===== PING SWEEP =====")
    subnet = input("Enter subnet (e.g., 192.168.1): ").strip()
    threads = []
    parts = subnet.split(".")

    if len(parts) != 3:
        print("\nEnter subnet like: 192.168.1")
        return

    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        t = threading.Thread(target=ping_host, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nPing Sweep Completed")
