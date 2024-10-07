# scanner/admin.py
from django.contrib import admin
from .models import Target, Vulnerability, ScanReport, Notification

admin.site.register(Target)
admin.site.register(Vulnerability)
admin.site.register(ScanReport)
admin.site.register(Notification)