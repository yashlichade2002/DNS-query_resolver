from django.contrib import admin
from .models import DNSQuery, DNSRecord

admin.site.register(DNSQuery)
admin.site.register(DNSRecord)

# Register your models here.
