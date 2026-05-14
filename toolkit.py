from modules.hash_generator import hash_menu
from modules.whois_lookup import whois_menu
from modules.dns_enum import dns_menu

print("1. Hash Generator")
print("2. WHOIS Lookup")
print("3. DNS Enumeration")

choice = input("Enter choice: ")

if choice == "1":
    hash_menu()

elif choice == "2":
    whois_menu()

elif choice == "3":
    dns_menu()

else:
    print("Invalid choice")
