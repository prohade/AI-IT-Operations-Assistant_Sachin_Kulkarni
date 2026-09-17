# AI IT Operations Assistant

A local **Agentic AI IT Support Assistant** built with **Python, OpenAI, LangGraph, SQLite, and Streamlit**.

The project demonstrates how an AI agent can understand a natural-language IT support request, decide whether a tool is required, call the appropriate local tool, preserve conversation context, validate actions, and return a user-friendly response.

## Project Objective

IT support users commonly need help with troubleshooting, checking existing support tickets, and creating new tickets. Traditional workflows often require users to navigate multiple screens or know which IT service to use.

This project provides a conversational assistant that can:

- understand an employee's IT support request;
- decide whether information retrieval or an action is required;
- select and execute the appropriate tool;
- access local employee, knowledge-base, and ticket data;
- preserve relevant context across multiple conversation turns;
- validate information before creating a ticket;
- prevent unnecessary duplicate tickets; and
- generate a clear final response based on tool results.

## Core Capabilities

- **Knowledge Search** — searches the local IT knowledge base.
- **Employee Lookup** — validates and retrieves employee information.
- **Ticket Lookup** — retrieves existing support-ticket details.
- **Duplicate Ticket Check** — checks for similar active tickets before creation.
- **Ticket Creation** — creates a new support ticket in the local SQLite database.
- **Tool / Function Calling** — allows the LLM to invoke structured Python tools.
- **LangGraph Workflow** — uses state, nodes, edges, conditional routing, and tool execution.
- **Conversation State** — retains relevant context during a multi-turn conversation.
- **Streamlit Chat UI** — provides chat history, reset functionality, and tool/action visibility.
- **Validation and Error Handling** — handles missing information, invalid records, duplicates, and failures without inventing data.

## Architecture

```text
                         ┌───────────────────────┐
                         │      User Request     │
                         └───────────┬───────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │     Streamlit UI      │
                         └───────────┬───────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │   LangGraph State     │
                         │ / Conversation Context│
                         └───────────┬───────────┘
                                     │
                                     v
                         ┌───────────────────────┐
                         │ OpenAI Agent / LLM    │
                         │ Intent + Tool Decision│
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
              No tool required                  Tool required
                    │                                 │
                    │                                 v
                    │                    ┌────────────────────────┐
                    │                    │   Tool Execution Node  │
                    │                    └────────────┬───────────┘
                    │                                 │
                    │        ┌────────────┬───────────┼────────────┬────────────┐
                    │        v            v           v            v            v
                    │   Knowledge     Employee      Ticket      Duplicate      Ticket
                    │    Search        Lookup       Lookup        Check       Creation
                    │        │            │           │            │            │
                    │        └────────────┴───────────┴────────────┴────────────┘
                    │                                 │
                    │                                 v
                    │                         ┌───────────────┐
                    │                         │ Local SQLite  │
                    │                         │   Database    │
                    │                         └───────┬───────┘
                    │                                 │
                    └────────────────┬────────────────┘
                                     v
                         ┌───────────────────────┐
                         │   Final AI Response   │
                         └───────────────────────┘
```

See `docs/architecture.md` for additional architecture details.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic, tools, validation, and database access |
| OpenAI API | Natural-language understanding and tool/function decisions |
| LangGraph | Agent workflow orchestration, state, nodes, edges, and routing |
| LangChain / `langchain-openai` | OpenAI model integration and tool binding |
| SQLite | Local employee, knowledge-base, and ticket data |
| Streamlit | Web-based conversational user interface |
| Pydantic | Structured data models and validation |
| python-dotenv | Local environment-variable loading |

## Project Structure

```text
AI-IT-Operations-Assistant/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── stage3_smoke_test.py
├── stage4_smoke_test.py
│
├── agent/
│   ├── graph.py
│   ├── prompts.py
│   ├── state.py
│   └── tool_registry.py
│
├── config/
│   └── settings.py
│
├── tools/
│   ├── knowledge_search.py
│   ├── employee_lookup.py
│   ├── ticket_lookup.py
│   ├── duplicate_check.py
│   └── ticket_creation.py
│
├── database/
│   ├── database.py
│   ├── schema.sql
│   └── seed.py
│
├── data/
│   └── support.db
│
├── tests/
│   └── test_stage4_readonly.py
│
└── docs/
    ├── architecture.md
    ├── demo_scenarios.md
    └── test_cases.md
```

> `.env`, `.venv/`, cache files, and other local/private files must not be committed to GitHub.

## Prerequisites

- Python installed on the local machine
- Internet connectivity for OpenAI API requests
- An OpenAI API key
- Git, if cloning the project from GitHub

## Environment Variables

Create a local `.env` file in the project root. Use `.env.example` as the template.

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.6
```

**Security:** Never commit `.env` or a real API key to GitHub. Only `.env.example` should contain placeholder values.

## Setup Instructions

### 1. Open the project folder

Example on Windows PowerShell:

```powershell
cd "C:\GenAI-Practice-All\Capstone Final Project\AI-IT-Operations-Assistant"
```

### 2. Create a virtual environment if one does not already exist

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```powershell
python -m pip install -U -r requirements.txt
```

### 5. Configure the OpenAI API key

Copy `.env.example` to `.env` and replace the placeholder API key with your own key.

### 6. Prepare the local sample database

If `data/support.db` is not present, or if you intentionally want to reset the project to its original sample data, run:

```powershell
python -m database.seed
```

Do **not** reseed the database if you want to preserve tickets created during a demonstration.

## Run the Tests

Run the local smoke test:

```powershell
python stage4_smoke_test.py
```

Run the assessment-oriented unit tests:

```powershell
python -m unittest tests.test_stage4_readonly -v
```

These local checks are designed to validate project components without making an OpenAI API request.

## Run the Application

Activate the virtual environment and start Streamlit:

```powershell
.venv\Scripts\activate
python -m streamlit run app.py --server.fileWatcherType none
```

Streamlit will display a local URL in the terminal, normally:

```text
http://localhost:8501
```

Press `Ctrl + C` in the terminal to stop the application.

## Example Test Scenarios

### 1. Knowledge Search

**Input**

```text
How do I reset my VPN password?
```

**Expected behavior:** The agent selects the knowledge-search tool, retrieves the relevant local knowledge-base information, and returns troubleshooting steps.

### 2. Ticket Lookup

**Input**

```text
What is the status of my VPN issue? My employee ID is EMP1024.
```

**Expected behavior:** The agent uses the employee/ticket information available to it and returns retrieved ticket details without inventing missing information.

### 3. Multi-turn Ticket Creation

**Turn 1**

```text
My laptop camera is not working. Please create a ticket.
```

If required information is missing, the assistant asks for it.

**Turn 2**

```text
EMP1030
```

**Expected behavior:** Relevant information from the conversation is retained, the employee is validated, duplicate checking is performed, and ticket creation proceeds only when the required information is available.

### 4. Duplicate Prevention

**Input**

```text
My VPN keeps disconnecting. Please create a ticket. My employee ID is EMP1024.
```

**Expected behavior:** The application checks for a similar active ticket and avoids creating an unnecessary duplicate when a matching active ticket is found.

### 5. Missing Information / Validation

**Input**

```text
Please create a ticket.
```

**Expected behavior:** The assistant requests the required information instead of blindly creating a ticket.

## How the Project Demonstrates the Required Concepts

| Requirement | Demonstration in This Project |
|---|---|
| Python | Implements the UI, agent workflow, tools, validation, and database operations |
| LangGraph | Orchestrates the graph using state, nodes, edges, and routing |
| Agentic AI | The LLM interprets requests and decides which action/tool is required |
| Tool Calling | The agent selects registered tools such as knowledge search or ticket creation |
| Function Calling | Tool arguments are passed using structured model/tool interfaces |
| State Management | Conversation context is maintained across turns |
| Conditional Routing | Workflow execution changes according to the agent/tool state |
| Local Data / Database Integration | SQLite stores employees, knowledge articles, and tickets |
| Prompt Engineering | Agent behavior, tool-use rules, and safety constraints are defined in prompts |
| Streamlit | Provides the conversational web interface |
| Error Handling | Missing data, invalid records, duplicates, and failures are handled explicitly |
| Modular Architecture | Agent, tools, database, configuration, tests, and UI are separated into modules |

## Key Design Decisions

1. **Local SQLite data** keeps the project self-contained and avoids dependence on enterprise ITSM infrastructure.
2. **LLM decides, tools execute** separates natural-language reasoning from deterministic business operations.
3. **Structured tool responses** reduce the risk of unsupported ticket information and simplify response generation.
4. **Duplicate prevention** checks for similar active tickets before creating a new one.
5. **Conversation state** enables multi-turn workflows where information supplied in one turn can be reused later.
6. **API key isolation** keeps credentials in `.env` rather than source code.
7. **Modular components** make the application easier to understand, test, maintain, and extend.

## Safety and Validation

The assistant is designed not to blindly execute every requested action. The workflow:

- validates required information before ticket creation;
- checks employee information;
- checks for unnecessary duplicate tickets;
- asks for missing information;
- reports tool/database failures rather than pretending an action succeeded;
- uses ticket information returned by tools instead of inventing ticket IDs or statuses; and
- distinguishes retrieved information from generated recommendations where appropriate.

## Limitations

- The application uses fictional/local sample data rather than a production ITSM platform.
- Conversation state is intended for the active application/session and is not a permanent enterprise memory store.
- Knowledge search is based on the project's local search implementation rather than a production-scale semantic/vector search service.
- Duplicate detection is simplified for demonstration purposes and may require more advanced matching in production.
- Ticket assignment and escalation are simplified.
- OpenAI API access and internet connectivity are required for LLM-driven agent decisions.
- The project is an educational/local demonstration and does not integrate with real enterprise identity, ticketing, or monitoring systems.

## Documentation

Additional project documentation is available in:

- `docs/architecture.md` — workflow and architecture details
- `docs/demo_scenarios.md` — demonstration scenarios
- `docs/test_cases.md` — test cases and expected behavior

## Project Status

The application has progressed through the planned development stages and includes the agent workflow, local tools/database integration, conversation state, validation, testing, Streamlit interface, and assessment documentation required for the final project demonstration.

## Security Notes

Before pushing the project to GitHub:

1. Confirm `.env` is ignored by Git.
2. Confirm `.env.example` contains only placeholder values.
3. Do not commit `.venv/`, Python cache files, logs, or API keys.
4. Review `git status` before every commit containing configuration changes.

## Future Enhancements

Possible production-oriented extensions include:

- integration with a real ITSM platform;
- vector/embedding-based knowledge retrieval;
- authentication and role-based access;
- persistent conversation storage;
- ticket escalation and assignment rules;
- system-health/monitoring tools;
- audit logging and observability; and
- additional enterprise support tools.

---

**Project:** AI IT Operations Assistant  
**Type:** Agentic AI / Generative AI Application  
**Interface:** Streamlit  
**Workflow:** LangGraph  
**Data Store:** SQLite
