# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    subdomain = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    cidr = models.CharField(max_length=18, null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Description field for additional info
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the target was created

    def __str__(self):
        return self.target or 'Target'

    class Meta:
        verbose_name_plural = "Targets"
