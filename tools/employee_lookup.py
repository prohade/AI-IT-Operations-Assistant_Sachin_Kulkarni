from database.database import get_connection

def lookup_employee(employee_id: str) -> dict:
    if not employee_id or not employee_id.strip():
        return {"success": False, "error": "Employee ID is required."}
    employee_id = employee_id.strip().upper()
    try:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM employees WHERE UPPER(employee_id)=?", (employee_id,)).fetchone()
        if not row:
            return {"success": False, "found": False, "error": f"No employee found with ID {employee_id}."}
        return {"success": True, "found": True, "employee": dict(row)}
    except Exception as exc:
        return {"success": False, "error": f"Employee lookup failed: {exc}"}
