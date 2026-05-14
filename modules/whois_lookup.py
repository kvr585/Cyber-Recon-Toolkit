import whois
import tldextract
from urllib.parse import urlparse


def whois_menu():

    print("\n===== WHOIS LOOKUP =====")

    domain = input("Enter domain or URL: ").strip()

    # Convert URL to domain
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc

    # Extract root domain
    extracted = tldextract.extract(domain)
    domain = extracted.domain + "." + extracted.suffix

    # Basic validation
    if "." not in domain:
        print("\nInvalid domain name")
        return

    try:

        info = whois.whois(domain)

        registrar = info.registrar
        creation = info.creation_date
        expiration = info.expiration_date
        name_servers = info.name_servers

        # Handle list values returned by some WHOIS servers
        if isinstance(creation, list):
            creation = creation[0]

        if isinstance(expiration, list):
            expiration = expiration[0]

        print("\n===== WHOIS INFORMATION =====")

        print("Domain:", domain)

        print("Registrar:", registrar if registrar else "Not Available")

        print("Creation Date:", creation if creation else "Not Available")

        print("Expiration Date:", expiration if expiration else "Not Available")

        if name_servers:

            print("\nName Servers:")

            if isinstance(name_servers, (list, set)):
                for ns in name_servers:
                    print("-", ns)

            else:
                print(name_servers)

        else:
            print("\nName Servers: Not Available")

    except Exception as e:
        print("\nError:", e)
