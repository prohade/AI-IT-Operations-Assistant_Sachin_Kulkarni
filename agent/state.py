from typing import Optional
from langgraph.graph import MessagesState

class SupportState(MessagesState):
    """Shared LangGraph state for the IT support conversation."""
    employee_id: Optional[str]
