import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import DNSQuery, DNSRecord

# Define UserType (GraphQL Type for User Model)
class UserType(DjangoObjectType):
    class Meta:
        model = User

# Define DNSQueryType (GraphQL Type for DNSQuery Model)
class DNSQueryType(DjangoObjectType):
    class Meta:
        model = DNSQuery

# Define DNSRecordType (GraphQL Type for DNSRecord Model)
class DNSRecordType(DjangoObjectType):
    class Meta:
        model = DNSRecord

# Define Query (GraphQL Read Operations)
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_dns_queries = graphene.List(DNSQueryType)
    all_dns_records = graphene.List(DNSRecordType)

    # Resolver functions
    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_all_dns_queries(self, info):
        return DNSQuery.objects.all()

    def resolve_all_dns_records(self, info):
        return DNSRecord.objects.all()

# Create GraphQL Schema
schema = graphene.Schema(query=Query)
