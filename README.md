# Cyber Recon Toolkit

Cyber Recon Toolkit is a terminal-based cybersecurity and reconnaissance utility suite built for network analysis, security assessment, and forensic reporting.

## Overview

This toolkit combines multiple reconnaissance, scanning, and forensic utilities into a single integrated Python platform. It is designed for practical cybersecurity workflows, clean CLI interaction, modular expansion, and report generation.

## Features

### Reconnaissance Modules

- WHOIS Lookup
- DNS Enumeration
- Ping Sweep

### Scanning Modules

- TCP Port Scanner
- Log Analyzer

### Utility Modules

- Hash Generator
- Phishing URL Checker
- Combined Report Generator

### Reporting

- JSON report export
- CSV report export
- PDF report export
- Consolidated evidence collection

## Project Structure

```text
Cyber-Recon-Toolkit-main/
├── README.md
├── requirements.txt
├── toolkit.py
├── modules/
│   ├── dns_enum.py
│   ├── hash_generator.py
│   ├── log_analyzer.py
│   ├── phishing_checker.py
│   ├── ping_sweep.py
│   ├── port_scanner.py
│   ├── report_generator.py
│   └── whois_lookup.py
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kvr585/Cyber-Recon-Toolkit
cd Cyber-Recon-Toolkit-main
```

2. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python toolkit.py
```

## Required Packages

The toolkit uses the following Python packages:

- `rich`
- `python-whois`
- `tldextract`
- `dnspython`
- `requests`

These are already listed in `requirements.txt`.

## Running the Toolkit

Launch the toolkit from the project root:

```bash
python toolkit.py
```

## Main Menu

```text
RECON
1. WHOIS Lookup
2. DNS Enumeration
3. Ping Sweep

SCANNING
4. Port Scanner
5. Log Analyzer

UTILITIES
6. Hash Generator
7. Phishing URL Checker
8. Generate Combined Report

SYSTEM
9. Exit
```

## Module Details

### WHOIS Lookup

- Domain WHOIS lookup
- Registrar information
- Creation and expiration dates
- Domain status
- DNS nameservers
- JSON report generation

### DNS Enumeration

- A record lookup
- AAAA record lookup
- MX record lookup
- NS record lookup
- TXT record lookup
- CNAME discovery
- DNS summary output
- JSON report export

### Ping Sweep

- /24 subnet discovery
- Multithreaded ICMP scanning
- Live host detection
- Scan timing
- JSON reporting

### Port Scanner

- Multithreaded TCP port scanning
- Custom port range support
- Service detection
- Basic banner grabbing
- Progress output
- JSON reporting

### Log Analyzer

- Log file parsing
- Suspicious activity detection
- Error highlighting
- Security event inspection
- JSON export

### Hash Generator

- MD5, SHA1, SHA256, SHA512 hashing
- Text hashing
- File hashing
- Hash verification
- File integrity checks
- JSON report export

### Phishing URL Checker

- URL structure analysis
- Suspicious keyword detection
- IP-based URL detection
- URL length checks
- HTTPS validation

### Combined Report Generator

- Aggregates module outputs into combined JSON
- Generates combined CSV reports
- Produces formatted PDF reports
- Includes structured summary and timestamps

## Output and Reports

Generated reports are saved to the project output folder when available. Supported formats include JSON, CSV, and PDF.

## License

This project is intended for educational and academic use only. Use responsibly and only perform authorized security testing.
