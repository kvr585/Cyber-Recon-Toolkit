from modules.hash_generator import hash_menu
from modules.whois_lookup import whois_menu
from modules.dns_enum import dns_menu
from modules.port_scanner import port_scan_menu
from modules.ping_sweep import ping_sweep_menu

print("1. Hash Generator")
print("2. WHOIS Lookup")
print("3. DNS Enumeration")
print("4. Port Scanner")
print("5. Ping Sweep")

choice = input("Enter choice: ")

if choice == "1":
    hash_menu()

elif choice == "2":
    whois_menu()

elif choice == "3":
    dns_menu()

elif choice == "4":
    port_scan_menu()
    
elif choice == "5":
    ping_sweep_menu()

else:
    print("Invalid choice")
