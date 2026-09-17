from pprint import pprint
from tools.knowledge_search import search_knowledge
from tools.employee_lookup import lookup_employee
from tools.ticket_lookup import lookup_tickets
from tools.duplicate_check import check_duplicate_ticket
from tools.ticket_creation import create_ticket

print("\n1. Knowledge Search")
pprint(search_knowledge("How do I reset my VPN password?"))
print("\n2. Employee Lookup")
pprint(lookup_employee("EMP1024"))
print("\n3. Ticket Lookup")
pprint(lookup_tickets("EMP1024"))
print("\n4. Duplicate Check")
pprint(check_duplicate_ticket("EMP1024", "VPN", "VPN disconnects frequently", "My VPN keeps disconnecting every few minutes."))
print("\n5. New Ticket Creation")
pprint(create_ticket("EMP1030", "Laptop", "Laptop camera is not working", "The built-in camera is not detected in Teams meetings.", "Medium"))
