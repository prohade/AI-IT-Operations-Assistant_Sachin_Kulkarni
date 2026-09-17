import unittest

from tools.employee_lookup import lookup_employee
from tools.knowledge_search import search_knowledge
from tools.ticket_lookup import lookup_tickets
from tools.duplicate_check import check_duplicate_ticket
from tools.ticket_creation import create_ticket


class Stage4ReadOnlyTests(unittest.TestCase):
    """Assessment-oriented checks that avoid creating a new database ticket."""

    def test_employee_lookup(self):
        result = lookup_employee("EMP1024")
        self.assertTrue(result.get("success"))
        self.assertTrue(result.get("found"))

    def test_knowledge_search(self):
        result = search_knowledge("reset VPN password")
        self.assertTrue(result.get("success"))
        self.assertTrue(result.get("found"))

    def test_ticket_lookup(self):
        result = lookup_tickets("EMP1024")
        self.assertTrue(result.get("success"))
        self.assertGreaterEqual(result.get("count", 0), 1)

    def test_missing_required_ticket_fields_are_blocked(self):
        result = create_ticket("", "Laptop", "Camera issue", "Camera not working")
        self.assertFalse(result.get("success"))
        self.assertIn("required", result.get("error", "").lower())

    def test_duplicate_check_executes_safely(self):
        result = check_duplicate_ticket(
            "EMP1024",
            "VPN",
            "VPN disconnects frequently",
            "VPN keeps disconnecting every few minutes.",
        )
        self.assertTrue(result.get("success"))
        self.assertIn("duplicate_found", result)


if __name__ == "__main__":
    unittest.main()
