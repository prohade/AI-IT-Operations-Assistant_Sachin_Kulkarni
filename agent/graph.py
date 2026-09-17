import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from agent.prompts import SYSTEM_PROMPT
from agent.state import SupportState
from agent.tool_registry import TOOLS
from config.settings import settings

_EMPLOYEE_PATTERN = re.compile(r"\bEMP\s*[-:]?\s*(\d{3,8})\b", re.IGNORECASE)


def capture_context(state: SupportState) -> dict:
    """Capture structured context such as employee ID from the latest user turn."""
    messages = state.get("messages", [])
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            text = str(message.content)
            match = _EMPLOYEE_PATTERN.search(text)
            if match:
                return {"employee_id": f"EMP{match.group(1)}".upper()}
            break
    return {}


def build_support_graph():
    # GPT-5.6 function tools through the Chat Completions path require
    # reasoning_effort="none" in this project configuration.
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=0,
        api_key=settings.openai_api_key,
        reasoning_effort="none",
    )
    llm_with_tools = llm.bind_tools(TOOLS)

    def agent_node(state: SupportState) -> dict:
        employee_id = state.get("employee_id")
        context = SYSTEM_PROMPT
        if employee_id:
            context += f"\nCurrent remembered employee ID: {employee_id}."

        response = llm_with_tools.invoke(
            [SystemMessage(content=context)] + list(state.get("messages", []))
        )
        return {"messages": [response]}

    def route_after_agent(state: SupportState):
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "tools"
        return END

    workflow = StateGraph(SupportState)
    workflow.add_node("capture_context", capture_context)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(TOOLS, handle_tool_errors=True))

    workflow.add_edge(START, "capture_context")
    workflow.add_edge("capture_context", "agent")
    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {"tools": "tools", END: END},
    )
    workflow.add_edge("tools", "agent")

    memory = InMemorySaver()
    return workflow.compile(checkpointer=memory)
