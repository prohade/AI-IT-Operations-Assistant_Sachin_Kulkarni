from database.database import get_connection

def lookup_tickets(employee_id: str, ticket_id=None, status=None, category=None) -> dict:
    if not employee_id or not employee_id.strip():
        return {"success": False, "error": "Employee ID is required."}
    sql = "SELECT * FROM tickets WHERE UPPER(employee_id)=?"
    params = [employee_id.strip().upper()]
    if ticket_id:
        sql += " AND UPPER(ticket_id)=?"
        params.append(ticket_id.strip().upper())
    if status:
        sql += " AND LOWER(status)=?"
        params.append(status.strip().lower())
    if category:
        sql += " AND LOWER(category)=?"
        params.append(category.strip().lower())
    sql += " ORDER BY created_at DESC"
    try:
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        tickets = [dict(r) for r in rows]
        return {"success": True, "found": bool(tickets), "count": len(tickets), "tickets": tickets}
    except Exception as exc:
        return {"success": False, "error": f"Ticket lookup failed: {exc}"}
