# models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Target(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    subdomain = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    cidr = models.CharField(max_length=18, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url or self.ip_address or self.domain or 'Target'

    class Meta:
        verbose_name_plural = "Targets"

class Vulnerability(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='vulnerabilities')
    name = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    confidence = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Open')
    discovered_date = models.DateTimeField(auto_now_add=True)

class ScanReport(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    scan_date = models.DateTimeField(auto_now_add=True)
    pdf_report = models.FileField(upload_to='reports/')
    status = models.CharField(max_length=50, default='In Progress')

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)