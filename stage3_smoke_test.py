"""Local smoke tests for the graph structure and tools; does not call OpenAI."""
from agent.graph import capture_context
from langchain_core.messages import HumanMessage
from database.seed import seed_database
from tools.employee_lookup import lookup_employee
from tools.knowledge_search import search_knowledge
from tools.ticket_lookup import lookup_tickets
from tools.duplicate_check import check_duplicate_ticket

seed_database()

assert capture_context({"messages": [HumanMessage(content="My ID is EMP1024")]})["employee_id"] == "EMP1024"
assert lookup_employee("EMP1024")["success"]
assert search_knowledge("VPN password reset")["found"]
assert lookup_tickets("EMP1024")["count"] >= 1
assert check_duplicate_ticket(
    "EMP1024", "VPN", "VPN disconnects frequently", "VPN keeps disconnecting"
)["duplicate_found"]

print("Stage 3 local smoke tests passed. OpenAI was not called.")
