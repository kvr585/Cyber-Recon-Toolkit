import os
import json
import re
import socket
from datetime import datetime

from rich import print
from rich.console import Console

from modules.dns_enum import dns_lookup
from modules.port_scanner import run_port_scan, is_valid_target
from modules.report_generator import add_watermark, open_report_file
from modules.phishing_checker import analyze_url
from modules.whois_lookup import whois_lookup

from reportlab.lib.colors import grey, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table as RLTable, TableStyle

console = Console()


def is_ip(target):
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, target)
            return True
        except socket.error:
            return False


def normalize_target(target):
    if target.startswith(("http://", "https://")):
        target = re.sub(r"^https?://", "", target).strip("/ ")
    return target


def calculate_risk_score(report_data):
    score = 0
    open_ports = report_data.get("port_scan") or {}
    open_ports_count = len(open_ports)

    if open_ports_count > 10:
        score += 3
    elif open_ports_count > 3:
        score += 2
    elif open_ports_count > 0:
        score += 1

    dangerous_port_weights = {
        21: 2,
        23: 3,
        3389: 2,
    }

    for port_str in open_ports:
        try:
            port = int(port_str)
            score += dangerous_port_weights.get(port, 0)
        except ValueError:
            continue

    phishing_issues = report_data.get("phishing_analysis") or []
    score += len(phishing_issues)

    return score


def get_risk_rating(score):
    if score >= 8:
        return "HIGH"
    if score >= 4:
        return "MEDIUM"
    return "LOW"


def build_summary_table(report_data, risk_level):
    open_ports = len(report_data.get("port_scan") or {})
    dns_records = sum(len(records) for records in (report_data.get("dns") or {}).values())
    phishing_findings = len(report_data.get("phishing_analysis") or [])
    return [
        ["Target", report_data.get("target", "N/A")],
        ["Open Ports", str(open_ports)],
        ["DNS Records", str(dns_records)],
        ["Phishing Findings", str(phishing_findings)],
        ["Risk Level", risk_level],
    ]


def generate_pdf_report(report_data, risk_level, output_file):
    try:
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontSize=24,
            leading=28,
            textColor=HexColor("#1A365D"),
            spaceAfter=12,
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontSize=14,
            leading=18,
            textColor=HexColor("#4A5568"),
            spaceAfter=18,
        )

        section_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=HexColor("#2B6CB0"),
            spaceBefore=10,
            spaceAfter=8,
        )

        normal_style = styles["Normal"]

        elements = []
        elements.append(Paragraph("Cyber Recon Toolkit", title_style))
        elements.append(Paragraph("Automated Security Assessment", subtitle_style))
        elements.append(Spacer(1, 16))

        elements.append(Paragraph("Cover Page", section_style))
        elements.append(Paragraph(
            "This report summarizes the automated security assessment for the requested target.",
            normal_style,
        ))
        elements.append(Spacer(1, 18))

        elements.append(Paragraph("Target Information", section_style))
        elements.append(Paragraph(f"Target: {report_data.get('target', 'N/A')}", normal_style))
        elements.append(Paragraph(f"Assessment Timestamp: {report_data.get('timestamp', 'N/A')}", normal_style))
        elements.append(Paragraph(f"Risk Rating: <b>{risk_level}</b>", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Executive Summary", section_style))
        summary_text = (
            "This assessment aggregates WHOIS, DNS, port scanning, and phishing analysis "
            "to provide a concise security overview."
        )
        if risk_level == "LOW":
            summary_text += " The overall posture is low risk."
        elif risk_level == "MEDIUM":
            summary_text += " The overall posture is medium risk and should be reviewed."
        else:
            summary_text += " The overall posture is high risk and requires urgent attention."
        elements.append(Paragraph(summary_text, normal_style))
        elements.append(Spacer(1, 16))

        elements.append(Paragraph("Risk Level", section_style))
        elements.append(Paragraph(f"Overall Risk Rating: <b>{risk_level}</b>", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Assessment Summary", section_style))
        summary_table = RLTable(build_summary_table(report_data, risk_level), colWidths=[150, 360])
        summary_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, grey),
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#E2E8F0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#1A365D")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 16))

        elements.append(Paragraph("WHOIS Findings", section_style))
        if report_data.get("whois"):
            whois_lines = [
                f"Registrar: {report_data['whois'].get('registrar', 'N/A')}",
                f"Organization: {report_data['whois'].get('organization', 'N/A')}",
                f"Country: {report_data['whois'].get('country', 'N/A')}",
                f"Creation Date: {report_data['whois'].get('creation_date', 'N/A')}",
                f"Expiration Date: {report_data['whois'].get('expiration_date', 'N/A')}"
            ]
            elements.append(Paragraph("<br/>".join(whois_lines), normal_style))
        else:
            elements.append(Paragraph("No WHOIS findings available.", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("DNS Findings", section_style))
        if report_data.get("dns"):
            dns_lines = []
            for record_type, records in (report_data.get("dns") or {}).items():
                if records:
                    dns_lines.append(f"{record_type}: {', '.join(records)}")
            elements.append(Paragraph("<br/>".join(dns_lines) if dns_lines else "No DNS records retrieved.", normal_style))
        else:
            elements.append(Paragraph("No DNS findings available.", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Open Ports", section_style))
        ports_data = report_data.get("port_scan") or {}
        if ports_data:
            port_lines = []
            for port, details in sorted(ports_data.items(), key=lambda item: int(item[0])):
                banner = details.get("banner", "N/A")
                warning = details.get("warning", "")
                line = f"Port {port}: {details.get('service', 'Unknown')} - Banner: {banner}"
                if warning:
                    line += f" (Warning: {warning})"
                port_lines.append(line)
            elements.append(Paragraph("<br/>".join(port_lines), normal_style))
        else:
            elements.append(Paragraph("No open ports identified in the common range.", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Phishing Analysis", section_style))
        phishing_data = report_data.get("phishing_analysis")
        if phishing_data is None:
            elements.append(Paragraph("Phishing analysis not applicable.", normal_style))
        elif phishing_data:
            elements.append(Paragraph("Issues detected:", normal_style))
            elements.append(Paragraph("<br/>".join([f"• {issue}" for issue in phishing_data]), normal_style))
        else:
            elements.append(Paragraph("No phishing indicators detected.", normal_style))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Security Recommendations", section_style))
        recommendations = [
            "Review and close unnecessary open ports, especially high-risk services.",
            "Harden exposed services and enforce secure protocols.",
            "Investigate any phishing indicators and update security awareness controls.",
            "Monitor WHOIS and DNS configuration for unexpected changes.",
            "Retest the target after remediation to confirm the risk posture has improved."
        ]
        elements.append(Paragraph("<br/>".join(recommendations), normal_style))

        doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)
        return True
    except Exception as exc:
        print(f"[red]Failed to generate PDF report: {exc}[/red]")
        return False


def run_assessment(target):
    target = normalize_target(target)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_data = {
        "target": target,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "whois": None,
        "dns": None,
        "port_scan": {},
        "phishing_analysis": None,
    }

    target_is_domain = not is_ip(target)

    if target_is_domain:
        report_data["whois"] = whois_lookup(target, silent=True)
        report_data["dns"] = dns_lookup(target, silent=True)
        report_data["phishing_analysis"] = analyze_url(target, silent=True)

    report_data["port_scan"] = run_port_scan(target, 1, 1024, silent=True) or {}

    score = calculate_risk_score(report_data)
    risk_level = get_risk_rating(score)

    reports_folder = "reports"
    os.makedirs(reports_folder, exist_ok=True)

    json_filename = f"{reports_folder}/security_assessment_{timestamp}.json"
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(report_data, json_file, indent=4)

    pdf_filename = f"{reports_folder}/security_assessment_{timestamp}.pdf"
    generate_pdf_report(report_data, risk_level, pdf_filename)

    print(f"[bold green]JSON report saved:[/bold green] {json_filename}")
    print(f"[bold green]PDF report saved:[/bold green] {pdf_filename}")

    if target_is_domain:
        dns_record_count = sum(len(records) for records in (report_data.get("dns") or {}).values())
        phishing_findings = len(report_data.get("phishing_analysis") or [])
    else:
        dns_record_count = "N/A (IP Target)"
        phishing_findings = "N/A"

    print("\nAssessment Summary")
    print(f"Target: {report_data['target']}")
    print(f"Open Ports: {len(report_data['port_scan'])}")
    print(f"DNS Records: {dns_record_count}")
    print(f"Phishing Findings: {phishing_findings}")
    print(f"Risk Level: {risk_level}")

    return json_filename, pdf_filename


def security_assessment_menu():
    print("\n[bold cyan]===== AUTOMATED SECURITY ASSESSMENT =====[/bold cyan]")

    while True:
        target = console.input("\n[bold green]Enter target (domain or IP) >[/bold green] ").strip()
        if target.lower() in ["back", "exit", "quit"]:
            break

        target = normalize_target(target)

        if not is_valid_target(target):
            print("[red]Invalid target. Enter a valid IP or domain name.[/red]")
            continue

        json_report, pdf_report = run_assessment(target)

        while True:
            print("\n1. Open JSON Report")
            print("2. Open PDF Report")
            print("3. Run Another Assessment")
            print("4. Back to Main Menu")

            choice = console.input("\n[bold green]Choice >[/bold green] ").strip()
            if choice == "1":
                open_report_file(json_report)
            elif choice == "2":
                open_report_file(pdf_report)
            elif choice == "3":
                break
            elif choice == "4":
                return
            else:
                print("[red]Invalid choice[/red]")
