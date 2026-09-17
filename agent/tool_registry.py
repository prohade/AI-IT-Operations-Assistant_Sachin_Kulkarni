from langchain_core.tools import tool

from tools.knowledge_search import search_knowledge
from tools.employee_lookup import lookup_employee
from tools.ticket_lookup import lookup_tickets
from tools.duplicate_check import check_duplicate_ticket
from tools.ticket_creation import create_ticket


@tool
def knowledge_search(query: str) -> dict:
    """Search the local IT knowledge base for troubleshooting or how-to information."""
    return search_knowledge(query)


@tool
def employee_lookup(employee_id: str) -> dict:
    """Validate and retrieve an employee using an employee ID such as EMP1024."""
    return lookup_employee(employee_id)


@tool
def ticket_lookup(
    employee_id: str,
    ticket_id: str = "",
    status: str = "",
    category: str = "",
) -> dict:
    """Look up support tickets for an employee, optionally filtering by ticket ID, status, or category."""
    return lookup_tickets(
        employee_id=employee_id,
        ticket_id=ticket_id or None,
        status=status or None,
        category=category or None,
    )


@tool
def duplicate_ticket_check(
    employee_id: str,
    category: str,
    subject: str,
    description: str = "",
) -> dict:
    """Check whether an employee already has a similar active ticket."""
    return check_duplicate_ticket(employee_id, category, subject, description)


@tool
def create_support_ticket(
    employee_id: str,
    category: str,
    subject: str,
    description: str,
    priority: str = "Medium",
) -> dict:
    """Create an IT support ticket after employee validation and duplicate checking."""
    # Deliberately do not expose allow_duplicate to the LLM.
    return create_ticket(
        employee_id=employee_id,
        category=category,
        subject=subject,
        description=description,
        priority=priority,
        allow_duplicate=False,
    )


TOOLS = [
    knowledge_search,
    employee_lookup,
    ticket_lookup,
    duplicate_ticket_check,
    create_support_ticket,
]
