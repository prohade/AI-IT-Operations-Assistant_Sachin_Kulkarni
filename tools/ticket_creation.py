from datetime import datetime, timezone
from database.database import get_connection
from tools.employee_lookup import lookup_employee
from tools.duplicate_check import check_duplicate_ticket

def _next_ticket_id(conn):
    rows = conn.execute("SELECT ticket_id FROM tickets").fetchall()
    nums = [int(r["ticket_id"][3:]) for r in rows if r["ticket_id"].startswith("INC") and r["ticket_id"][3:].isdigit()]
    return f"INC{max(nums, default=10000) + 1:05d}"

def create_ticket(employee_id: str, category: str, subject: str, description: str, priority: str = "Medium", allow_duplicate: bool = False) -> dict:
    required = {"employee_id": employee_id, "category": category, "subject": subject, "description": description}
    missing = [k for k, v in required.items() if not v or not str(v).strip()]
    if missing:
        return {"success": False, "error": "Missing required information: " + ", ".join(missing)}
    employee_id = employee_id.strip().upper()
    category = category.strip().title()
    priority = (priority or "Medium").strip().title()
    if priority not in {"Low", "Medium", "High", "Critical"}:
        return {"success": False, "error": "Priority must be Low, Medium, High or Critical."}
    employee = lookup_employee(employee_id)
    if not employee.get("success"):
        return {"success": False, "error": f"Employee {employee_id} could not be validated."}
    dup = check_duplicate_ticket(employee_id, category, subject, description)
    if dup.get("duplicate_found") and not allow_duplicate:
        return {"success": False, "duplicate_found": True, "duplicates": dup["duplicates"], "error": "A similar active ticket already exists. Ticket creation stopped."}
    try:
        with get_connection() as conn:
            ticket_id = _next_ticket_id(conn)
            created_at = datetime.now(timezone.utc).isoformat()
            conn.execute("INSERT INTO tickets (ticket_id,employee_id,category,subject,description,priority,status,assigned_to,created_at) VALUES (?,?,?,?,?,?,?,?,?)", (ticket_id, employee_id, category, subject.strip(), description.strip(), priority, "Open", "IT Service Desk", created_at))
            conn.commit()
        return {"success": True, "ticket_created": True, "ticket": {"ticket_id": ticket_id, "employee_id": employee_id, "category": category, "subject": subject.strip(), "description": description.strip(), "priority": priority, "status": "Open", "assigned_to": "IT Service Desk", "created_at": created_at}}
    except Exception as exc:
        return {"success": False, "error": f"Ticket creation failed: {exc}"}
