import json
import uuid

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from agent.graph import build_support_graph
from config.settings import settings, validate_settings



st.set_page_config(
    page_title="AI IT Operations Assistant",
    
    page_icon="🤖",
    layout="wide",
)




@st.cache_resource
def get_graph():
    return build_support_graph()


def new_conversation():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.ui_messages = []


def message_text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") in {"text", "output_text"}:
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(p for p in parts if p)
    return str(content)


def collect_trace(messages):
    """Collect tool calls and tool results for the latest user turn."""
    start = 0
    for index in range(len(messages) - 1, -1, -1):
        if isinstance(messages[index], HumanMessage):
            start = index
            break

    trace = []
    for msg in messages[start + 1:]:
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            for call in msg.tool_calls:
                trace.append({
                    "type": "call",
                    "tool": call.get("name", "unknown"),
                    "args": call.get("args", {}),
                })
        elif isinstance(msg, ToolMessage):
            raw = msg.content
            try:
                parsed = json.loads(raw) if isinstance(raw, str) else raw
            except Exception:
                parsed = raw
            trace.append({
                "type": "result",
                "tool": getattr(msg, "name", None) or "tool",
                "result": parsed,
            })
    return trace


def friendly_error(exc: Exception) -> tuple[str, str]:
    """Return a safe user-facing message plus technical detail for debugging."""
    detail = str(exc)
    lower = detail.lower()

    if "api key" in lower or "authentication" in lower or "401" in lower:
        message = "OpenAI authentication failed. Check OPENAI_API_KEY in your .env file and restart the app."
    elif "rate limit" in lower or "429" in lower:
        message = "The OpenAI API is temporarily rate-limited. Please wait briefly and try again."
    elif "connection" in lower or "timeout" in lower:
        message = "The AI service could not be reached. Check your internet connection and try again."
    elif "reasoning_effort" in lower:
        message = "The configured model/tool mode is incompatible. Verify the Stage 4 agent/graph.py file is in place."
    else:
        message = "The assistant could not complete the request. Please try again or reset the conversation."

    return message, detail


if "thread_id" not in st.session_state:
    new_conversation()

ok, config_error = validate_settings()

with st.sidebar:
    st.header("Agent Status")
    st.write(f"**Model:** `{settings.openai_model}`")
    st.write("**Workflow:** LangGraph")
    st.write("**Memory:** Conversation thread state")
    st.write("**Data:** Local SQLite")

    if ok:
        st.success("OpenAI API key detected")
    else:
        st.error(config_error)

    if st.button("🧹 Clear / Reset Conversation", use_container_width=True):
        new_conversation()
        st.rerun()

    st.divider()
    st.markdown("**Assessment demo prompts**")
    st.code("How do I reset my VPN password?")
    st.code("What is the status of my VPN issue? My employee ID is EMP1024.")
    st.code("My laptop camera is not working. Please create a ticket.")
    st.code("My VPN keeps disconnecting. Please create a ticket. My employee ID is EMP1024.")

st.title("🤖 AI IT Operations Assistant")
st.caption("Agentic AI-Powered IT Support & Operations Assistant -(Capstone project done by Sachin Kulkarni for IIT Patna) ")

st.markdown(
    "Ask a support question in natural language. The agent decides which local tool to use, "
    "executes it through LangGraph, and returns a user-friendly answer."
)

if not ok:
    st.warning(
        "Add OPENAI_API_KEY to your existing .env file, then restart Streamlit. "
        "Never place the key directly in source code."
    )
    st.stop()

for item in st.session_state.ui_messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
        if item.get("trace"):
            with st.expander("🔧 Tool / action details"):
                st.json(item["trace"])

prompt = st.chat_input("Describe your IT issue or ask about a support ticket...")

if prompt:
    st.session_state.ui_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        graph = get_graph()
        config = {"configurable": {"thread_id": st.session_state.thread_id}}

        with st.chat_message("assistant"):
            with st.spinner("Understanding the request and selecting the appropriate tool..."):
                result = graph.invoke(
                    {"messages": [HumanMessage(content=prompt)]},
                    config=config,
                )

            final_ai = next(
                (
                    m
                    for m in reversed(result["messages"])
                    if isinstance(m, AIMessage) and not getattr(m, "tool_calls", None)
                ),
                None,
            )
            answer = message_text(final_ai) if final_ai else "I could not generate a final response."
            trace = collect_trace(result["messages"])

            st.markdown(answer)
            if trace:
                with st.expander("🔧 Tool / action details"):
                    st.json(trace)

        st.session_state.ui_messages.append({
            "role": "assistant",
            "content": answer,
            "trace": trace,
        })

    except Exception as exc:
        user_message, technical_detail = friendly_error(exc)
        with st.chat_message("assistant"):
            st.error(user_message)
            with st.expander("Technical details"):
                st.code(technical_detail)

        st.session_state.ui_messages.append({
            "role": "assistant",
            "content": user_message,
            "trace": [],
        })
