# scanner/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import subprocess
import json
from .models import Target, Vulnerability, ScanReport, Notification
from reportlab.pdfgen import canvas
import os

@shared_task
def run_scan(target_id):
    target = Target.objects.get(id=target_id)
    scan_command = []
    
    if target.url:
        scan_command = ['nmap', '-sV', '--script', 'vuln', target.url]
    elif target.ip_address:
        scan_command = ['nmap', '-sV', '--script', 'vuln', target.ip_address]
    elif target.domain:
        scan_command = ['nmap', '-sV', '--script', 'vuln', target.domain]
    
    try:
        # Run the scan
        scan_output = subprocess.run(
            scan_command,
            capture_output=True,
            text=True
        )
        
        # Parse results and create vulnerabilities
        vulns = parse_scan_results(scan_output.stdout)
        for vuln in vulns:
            Vulnerability.objects.create(
                target=target,
                name=vuln['name'],
                description=vuln['description'],
                severity=vuln['severity'],
                confidence=vuln['confidence']
            )
        
        # Generate PDF report
        report_path = generate_pdf_report(target, vulns)
        
        # Create scan report
        ScanReport.objects.create(
            target=target,
            pdf_report=report_path,
            status='Completed'
        )
        
        # Create notification
        Notification.objects.create(
            user=target.user,
            message=f'Scan completed for {target.url or target.ip_address or target.domain}'
        )
        
        # Send email
        send_mail(
            'Vulnerability Scan Completed',
            f'The vulnerability scan for your target has been completed. Please check your dashboard for results.',
            settings.DEFAULT_FROM_EMAIL,
            [target.user.email],
            fail_silently=False,
        )
        
    except Exception as e:
        # Handle errors
        Notification.objects.create(
            user=target.user,
            message=f'Scan failed for {target.url or target.ip_address or target.domain}: {str(e)}'
        )

def parse_scan_results(output):
    # Implement your parsing logic here based on your scanner's output format
    # This is a placeholder implementation
    return [
        {
            'name': 'Sample Vulnerability',
            'description': 'Description of the vulnerability',
            'severity': 'HIGH',
            'confidence': 'High'
        }
    ]

def generate_pdf_report(target, vulnerabilities):
    filename = f'scan_report_{target.id}.pdf'
    filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
    
    c = canvas.Canvas(filepath)
    c.drawString(100, 800, f"Vulnerability Scan Report")
    c.drawString(100, 780, f"Target: {target.url or target.ip_address or target.domain}")
    
    y_position = 750
    for vuln in vulnerabilities:
        c.drawString(100, y_position, f"Vulnerability: {vuln['name']}")
        c.drawString(120, y_position - 20, f"Severity: {vuln['severity']}")
        y_position -= 40
    
    c.save()
    return f'reports/{filename}'