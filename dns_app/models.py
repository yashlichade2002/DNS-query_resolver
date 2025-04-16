from django.db import models
from django.contrib.auth.models import User  # Import built-in user model

class DNSQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Track user queries
    domain = models.CharField(max_length=255, db_index=True)  # Domain name queried
    ip_address = models.GenericIPAddressField()  # Resolved IP address
    timestamp = models.DateTimeField(auto_now_add=True)  # Query time

    def __str__(self):
        return f"{self.domain} -> {self.ip_address}"

class DNSRecord(models.Model):
    domain = models.CharField(max_length=255, unique=True)  # Unique domain entry
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.domain} -> {self.ip_address}"

# Create your models here.
