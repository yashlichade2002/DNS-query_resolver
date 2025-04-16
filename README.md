python3 manage.py runserver
http://127.0.0.1:8000/resolve/?domain=google.com // for ip address
http://127.0.0.1:8000/graphql/ //for grafhql
//put this query in grafhql 
query {
  allDnsQueries {
    domain
    ipAddress
    timestamp
  }
} //this is query to show all data of dns
