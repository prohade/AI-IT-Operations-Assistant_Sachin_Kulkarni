import re
from database.database import get_connection

OPEN_STATUSES = {"open", "in progress", "pending", "assigned"}

def _tokens(text):
    return set(re.findall(r"[a-zA-Z0-9]+", (text or "").lower()))

def check_duplicate_ticket(employee_id: str, category: str, subject: str, description: str = "") -> dict:
    if not employee_id or not employee_id.strip():
        return {"success": False, "error": "Employee ID is required."}
    if not category or not category.strip():
        return {"success": False, "error": "Category is required."}
    if not subject or not subject.strip():
        return {"success": False, "error": "Subject is required."}
    target = _tokens(subject + " " + description)
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM tickets WHERE UPPER(employee_id)=? AND LOWER(category)=?", (employee_id.strip().upper(), category.strip().lower())).fetchall()
        duplicates = []
        for row in rows:
            ticket = dict(row)
            if ticket["status"].lower() not in OPEN_STATUSES:
                continue
            existing = _tokens(ticket["subject"] + " " + ticket["description"])
            similarity = len(target & existing) / len(target) if target else 0
            if similarity >= 0.30:
                ticket["similarity_score"] = round(similarity, 2)
                duplicates.append(ticket)
        return {"success": True, "duplicate_found": bool(duplicates), "duplicates": duplicates}
    except Exception as exc:
        return {"success": False, "error": f"Duplicate check failed: {exc}"}
