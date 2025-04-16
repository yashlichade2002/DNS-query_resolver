from django.shortcuts import render

# Create your views here.
import dns.message
import dns.query
import dns.resolver
from django.http import JsonResponse
from .models import DNSRecord,DNSQuery
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the DNS Resolver!")

def resolve_dns(request):
    return HttpResponse("DNS Resolver is working!")


# List of Root DNS Servers
ROOT_DNS_SERVERS = [
    "198.41.0.4",    # a.root-servers.net
    "199.9.14.201",  # b.root-servers.net
    "192.33.4.12",   # c.root-servers.net
]

def recursive_dns_lookup(domain, nameserver):
    
    try:
        query = dns.message.make_query(domain, dns.rdatatype.A)  # Create DNS query
        response = dns.query.udp(query, nameserver, timeout=3)  # Send query over UDP

        # If response contains an answer, return the first IP
        if response.answer:
            for answer in response.answer:
                for item in answer.items:
                    if isinstance(item, dns.rdtypes.IN.A.A):
                        return item.address  # Return resolved IP

        # If no direct answer, check for referrals (next nameserver to query)
        if response.additional:
            for additional in response.additional:
                for item in additional.items:
                    if isinstance(item, dns.rdtypes.IN.A.A):
                        return recursive_dns_lookup(domain, item.address)  # Query next server

    except Exception as e:
        print(f"Error resolving {domain}: {str(e)}")
        return None  # Return None on failure

@login_required
def resolve_dns(request):
    """
    API endpoint that resolves a domain name to an IP address.
    Uses caching for efficiency and performs recursive resolution if needed.
    """
    domain = request.GET.get("domain")

    if not domain:
        return JsonResponse({"error": "Domain parameter is required"}, status=400)

    # Check if domain exists in cache
    try:
        record = DNSRecord.objects.get(domain=domain)
        DNSQuery.objects.create(user=request.user, domain=domain, ip_address=record.ip_address)
        return JsonResponse({"domain": record.domain, "ip": record.ip_address, "source": "cache"})
    except DNSRecord.DoesNotExist:
        pass  # Not found, proceed to recursive resolution

    # Start recursive DNS resolution using root servers
    for root_server in ROOT_DNS_SERVERS:
        ip_address = recursive_dns_lookup(domain, root_server)
        if ip_address:
            # Save to database for caching
            DNSRecord.objects.create(domain=domain, ip_address=ip_address)
            DNSQuery.objects.create(user=request.user, domain=domain, ip_address=ip_address)
            return JsonResponse({"domain": domain, "ip": ip_address, "source": "resolved"})

    return JsonResponse({"error": "Unable to resolve domain"}, status=400)
