import dns.resolver
from urllib.parse import urlparse


def dns_menu():

    print("\n===== DNS ENUMERATION =====")

    domain = input("Enter domain or URL: ").strip()

    # Convert URL to domain
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc

    print("\n===== DNS RECORDS =====")

    record_types = ["A", "MX", "NS", "TXT"]

    for record in record_types:

        print(f"\n{record} Records:")

        try:

            answers = dns.resolver.resolve(domain, record)

            for answer in answers:
                print("-", answer.to_text())

        except dns.resolver.NoAnswer:
            print("No records found")

        except dns.resolver.NXDOMAIN:
            print("Domain does not exist")

        except dns.resolver.Timeout:
            print("Request timed out")

        except Exception as e:
            print("Error:", e)