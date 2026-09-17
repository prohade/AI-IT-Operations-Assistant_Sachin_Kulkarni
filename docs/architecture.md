# Architecture

## High-level design

```mermaid
flowchart TD
    U[User / Streamlit Chat] --> S[LangGraph State]
    S --> C[Capture Context Node]
    C --> A[OpenAI Agent / Decision Node]
    A -->|Tool call| T[Tool Node]
    T --> K[Knowledge Search]
    T --> E[Employee Lookup]
    T --> L[Ticket Lookup]
    T --> D[Duplicate Check]
    T --> N[Ticket Creation]
    K --> DB[(Local SQLite)]
    E --> DB
    L --> DB
    D --> DB
    N --> DB
    DB --> T
    T --> A
    A -->|No tool call| F[Final Response]
    F --> U
```

## LangGraph elements demonstrated

- **State:** conversation messages plus remembered employee ID.
- **Nodes:** context capture, agent/decision node, and tool-execution node.
- **Edges:** start → context → agent; tools → agent.
- **Conditional routing:** the graph routes to tools only when the model emits a tool call; otherwise it ends with the final answer.
- **Tool execution:** all business data comes from local tools and SQLite.
- **Memory:** `InMemorySaver` persists state within a Streamlit conversation thread using `thread_id`.

## Safety design

Ticket creation validates required data and the employee before insertion. A duplicate check runs before ticket creation. Tool failures return structured results. The assistant is instructed not to invent ticket information and should clearly distinguish retrieved records from generated guidance.
