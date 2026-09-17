"""Local Stage 4 smoke test. Does not make an OpenAI API call."""

from agent.graph import build_support_graph
from config.settings import settings
from tools.employee_lookup import lookup_employee
from tools.knowledge_search import search_knowledge
from tools.ticket_lookup import lookup_tickets


def main():
    assert settings.openai_model, "OPENAI_MODEL is not configured."
    assert lookup_employee("EMP1024").get("success")
    assert search_knowledge("reset vpn password").get("found")
    assert lookup_tickets("EMP1024").get("success")

    # Build the graph to catch imports/configuration problems without invoking OpenAI.
    build_support_graph()
    print("Stage 4 local smoke tests passed. OpenAI was not called.")


if __name__ == "__main__":
    main()
