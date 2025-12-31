# Claude Code Development Guide

> **For Developers Using Claude Code**
> This file contains development guidelines and rules for contributing to this project.

## Overview

This project was built using [Claude Code](https://claude.ai/code), specializing in **Spec-Driven Development (SDD)** and **Agentic Development**.

### What is Claude Code?

Claude Code is an AI assistant that helps developers:
- Plan and architect features before coding
- Write tests first (TDD approach)
- Generate clean, well-documented code
- Maintain high code quality standards
- Follow consistent development workflows

---

## Monorepo Architecture

**This is a MONOREPO containing 3 phases of the Todo Application:**

### Phase 1: CLI Todo App (Completed)
- **Location**: `phase-1/`
- **Tech**: Python CLI with in-memory storage
- **Features**: 12 features with selection menus (F001-F013)
- **Tests**: 117 passing tests, ~51% coverage
- **Constitution**: `.specify/memory/constitution.md` (v2.1.0)

### Phase 2: Full-Stack Web App (Completed)
- **Frontend**: Next.js web UI (`frontend-web/`, port 3000)
- **Backend**: FastAPI REST API (`backend/src/`, port 8000)
- **Database**: Neon PostgreSQL: Authentication, Task CRUD, Modern UI/UX
- **Constitution**: `.specify/memory/phase-2-constitution.md` (v1.1.0)

### Phase 3: AI Chatbot (In Progress)
- **Frontend**: React ChatKit UI (`frontend-chatbot/`, port 3001)
- **Backend**: MCP Server (`backend/mcp/`) with OpenAI Agents SDK
- **Features**: Natural language task management
- **Constitution**: `.specify/memory/phase-3-constitution.md` (v1.1.0)

### Shared Components

```
To-do-app/  (Monorepo Root)
├── phase-1/              # Phase 1: Python CLI Todo App
│   ├── main.py           # CLI entry point
│   ├── src/todo/         # Core business logic
│   ├── tests/            # 117 tests
│   └── demo.py           # Feature demonstration
│
├── backend/              # Phase 2 & 3: FastAPI Backend
│   ├── src/api/
│   │   ├── main.py       # FastAPI app, CORS, startup
│   │   ├── config.py     # Pydantic settings
│   │   ├── auth.py       # JWT verification
│   │   ├── db.py         # SQLModel engine, sessions
│   │   ├── models.py     # User, Task, Tag, Conversation, Message
│   │   ├── routes/       # REST endpoints
│   │   │   ├── auth.py   # Auth endpoints
│   │   │   ├── tasks.py  # Task CRUD
│   │   │   ├── tags.py   # Tag management
│   │   │   └── chat.py   # Chat/session endpoints
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   │       ├── agent.py        # OpenAI agent
│   │       └── agent_client.py # Agent API client
│   ├── mcp/              # Phase 3: MCP Server tools
│   │   ├── server.py     # MCP server implementation
│   │   └── tools/        # 5 MCP tools (add_task, list_tasks, etc.)
│   └── tests/            # Backend tests
│
├── frontend-web/         # Phase 2: Next.js Web UI (port 3000)
│   ├── app/
│   │   ├── api/          # Better Auth API
│   │   ├── login/        # Login page
│   │   ├── signup/       # Signup page
│   │   ├── dashboard/    # Protected dashboard
│   │   └── page.tsx      # Landing page
│   ├── components/       # React components
│   ├── lib/              # API client, auth
│   └── types/            # TypeScript types
│
├── frontend-chatbot/     # Phase 3: React Chatbot (port 3001)
│   ├── src/
│   │   ├── components/   # ChatInterface
│   │   ├── lib/          # API client
│   │   └── pages/        # Next.js pages
│
├── specs/                # Feature specifications
│   ├── 001-todo-cli-app/
│   ├── 001-fullstack-web-app/
│   └── 002-ai-chatbot-mcp/
│
├── .spec-kit/            # Spec-Kit Plus configuration
│   ├── agents.yaml       # Agent/Skill definitions
│   ├── config.yaml       # Project configuration
│   └── skills/           # Reusable agent skills
│       └── auth_integration.md
│
├── history/prompts/      # Prompt History Records
├── history/adr/          # Architecture Decision Records
└── .specify/memory/      # Constitutions (all phases)
    ├── constitution.md           # Phase 1 (v2.1.0)
    ├── phase-2-constitution.md   # Phase 2 (v1.1.0)
    └── phase-3-constitution.md   # Phase 3 (v1.1.0)
```

---

## Constitution System

**Three constitutions govern this project, one per phase:**

| Phase | File | Version | Key Principles |
|-------|------|---------|----------------|
| 1 | `.specify/memory/constitution.md` | 2.1.0 | Three-tier architecture, TDD, in-memory storage |
| 2 | `.specify/memory/phase-2-constitution.md` | 1.1.0 | REST API, JWT auth, user isolation, agent-assisted dev |
| 3 | `.specify/memory/phase-3-constitution.md` | 1.1.0 | Radical statelessness, MCP tools, cloud-native |

### Constitution Usage

**Always reference the appropriate constitution for your phase:**

```
Phase 1 (CLI):     @.specify/memory/constitution.md
Phase 2 (Web):     @.specify/memory/phase-2-constitution.md
Phase 3 (Chatbot): @.specify/memory/phase-3-constitution.md
```

### Key Phase 3 Principles (Critical for AI Chatbot)

1. **Agentic Development Supremacy**: NO human shall write production code directly
2. **Radical Statelessness**: Server is a pure function - no memory between invocations
3. **MCP as Universal Interface**: All AI-to-app interactions through MCP tools only
4. **Four-Layer Architecture**: Presentation → API Gateway → Intelligence → Tool Execution
5. **Cloud-Native Ready**: Health checks, graceful shutdown, 0.0.0.0 binding

---

## Agent System (.spec-kit/agents.yaml)

The project uses specialized agents for validation, auditing, and code generation.

### Available Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **spec_validator** | Validate specifications before implementation | Before starting, after spec updates |
| **security_auditor** | Audit implementation for security vulnerabilities | After auth/API implementation |
| **api_contract_validator** | Ensure frontend-backend API alignment | After backend/frontend implementation |

### Available Skills

| Skill | Purpose | Output |
|-------|---------|--------|
| **jwt_middleware_generator** | Generate FastAPI JWT verification middleware | `backend/src/api/auth.py` |
| **api_client_generator** | Generate type-safe frontend API client | `frontend/lib/api.ts`, `frontend/types/api.ts` |
| **auth_integration** | Hardened JWT auth with Windows fixes | `backend/src/api/auth.py` |

### Agent vs Skill Usage

| Type | Purpose | Command Pattern |
|------|---------|-----------------|
| **Skill** | Generate boilerplate code | `"Use the <skill_name> skill to generate <file>"` |
| **Agent** | Validate existing code | `"Create the <agent_name> agent and RUN it"` |

**Examples:**
```
Skill:  "Use the jwt_middleware_generator skill to generate backend/src/api/auth.py"
Agent:  "Create the security_auditor agent and run it on backend/src/api/"
```

---

## MCP Tools Specification (Phase 3)

**Five atomic MCP tools for task management:**

### Tool 1: add_task
```python
def add_task(user_id: str, title: str, description: str = "") -> dict
```
- Insert new row in tasks table
- Return: `{"task_id": int, "status": "created", "title": str}`

### Tool 2: list_tasks
```python
def list_tasks(user_id: str, status: str = "all") -> dict
```
- Query tasks WHERE user_id = ? AND (completed filter)
- Return: `{"tasks": [...], "count": int, "filter": str}`

### Tool 3: complete_task
```python
def complete_task(user_id: str, task_id: int) -> dict
```
- UPDATE tasks SET completed=true WHERE id=? AND user_id=?
- Return: `{"task_id": int, "status": "completed", "title": str}`

### Tool 4: delete_task
```python
def delete_task(user_id: str, task_id: int) -> dict
```
- DELETE FROM tasks WHERE id=? AND user_id=?
- Return: `{"task_id": int, "status": "deleted", "title": str}`

### Tool 5: update_task
```python
def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> dict
```
- Build UPDATE query with provided fields
- Return: `{"task_id": int, "status": "updated", "title": str}`

**CRITICAL RULE:** MCP tools NEVER call each other. Agent orchestrates multi-tool workflows.

---

## How to Run This Project

### Three Services to Run

#### 1. Backend (FastAPI REST API + MCP Server)
```bash
cd backend
./venv/Scripts/python.exe -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```
- **Port**: http://localhost:8000
- **Health**: http://localhost:8000/health
- **Docs**: http://localhost:8000/docs

#### 2. Frontend Web (Next.js - Phase 2)
```bash
cd frontend-web
npm run dev
```
- **Port**: http://localhost:3000

#### 3. Frontend Chatbot (React - Phase 3)
```bash
cd frontend-chatbot
npm run dev
```
- **Port**: http://localhost:3001

### Port Summary

| Service | Port | URL | Status |
|---------|------|-----|--------|
| **Backend API** | 8000 | http://localhost:8000 | Ready |
| **Frontend Web** | 3000 | http://localhost:3000 | Ready |
| **Chatbot UI** | 3001 | http://localhost:3001 | Ready |
| **Database** | N/A | Neon PostgreSQL | Always available |

### Complete Startup Sequence (3 terminals)

**Terminal 1 (Backend):**
```bash
cd backend
./venv/Scripts/python.exe -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend Web):**
```bash
cd frontend-web
npm run dev
```

**Terminal 3 (Frontend Chatbot):**
```bash
cd frontend-chatbot
npm run dev
```

---

## Development Workflow

### Spec-Driven Development (SDD) Cycle

```
+--------------------------------------------------------+
| Phase 1: SPECIFICATION                                  |
| Write complete specs for architecture                   |
+---------------------+----------------------------------+
                      |
                      v
+--------------------------------------------------------+
| Phase 2: PLANNING (via Claude Code)                    |
| Generate implementation plan                           |
+---------------------+----------------------------------+
                      |
                      v
+--------------------------------------------------------+
| Phase 3: TASK BREAKDOWN (via Claude Code)              |
| Decompose plan into atomic tasks                       |
+---------------------+----------------------------------+
                      |
                      v
+--------------------------------------------------------+
| Phase 4: IMPLEMENTATION (via Claude Code)              |
| Execute each task via AI (TDD: Red-Green-Refactor)    |
+---------------------+----------------------------------+
                      |
                      v
+--------------------------------------------------------+
| Phase 5: VALIDATION (via Agents)                       |
| Run spec_validator, security_auditor, api_contract     |
+---------------------+----------------------------------+
                      |
                      v
+--------------------------------------------------------+
| Phase 6: REVIEW & DOCUMENTATION                         |
| Create PHR, ADR if significant decision                |
+--------------------------------------------------------+
```

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/sp.specify` | Create feature specification |
| `/sp.plan` | Generate architecture plan |
| `/sp.tasks` | Break into atomic tasks |
| `/sp.implement` | Execute implementation via TDD |
| `/sp.phr` | Create Prompt History Record |
| `/sp.adr <title>` | Create Architecture Decision Record |
| `/sp.clarify` | Identify underspecified areas |

---

## Prompt History Records (PHRs)

**After EVERY user interaction, create a PHR in `history/prompts/`:**

### PHR Routing

| Stage | Route |
|-------|-------|
| Constitution | `history/prompts/constitution/` |
| Spec | `history/prompts/<feature-name>/` |
| Plan | `history/prompts/<feature-name>/` |
| Tasks | `history/prompts/<feature-name>/` |
| Implementation (red/green/refactor) | `history/prompts/<feature-name>/` |
| General | `history/prompts/general/` |

### PHR Creation Process

1. Detect stage (constitution, spec, plan, tasks, red, green, refactor, etc.)
2. Generate title (3-7 words, slug format)
3. Read template from `.specify/templates/phr-template.prompt.md`
4. Allocate ID (increment, handle collisions)
5. Fill ALL placeholders:
   - ID, TITLE, STAGE, DATE_ISO, SURFACE
   - MODEL, FEATURE, BRANCH, USER
   - COMMAND, LABELS, LINKS
   - FILES_YAML (created/modified files)
   - TESTS_YAML (tests run/added)
   - PROMPT_TEXT (verbatim user input)
   - RESPONSE_TEXT (key assistant output)
6. Write file with Write tool
7. Report: ID, path, stage, title

---

## Architectural Decision Records (ADRs)

**For significant decisions, suggest documenting with ADR:**

```
+ Architectural decision detected: <brief-description>
   Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`
```

### Three-Part ADR Test

An ADR is needed when ALL are true:
- **Impact**: Long-term consequences (framework, data model, API, security)
- **Alternatives**: Multiple viable options considered
- **Scope**: Cross-cutting and influences system design

### ADR Location
`history/adr/<sequence>-<title>.md`

---

## Code Quality Standards

### Backend (Python)

| Tool | Purpose | Command |
|------|---------|---------|
| **black** | Formatting (line length: 88) | `black backend/` |
| **flake8** | Linting | `flake8 backend/` |
| **mypy** | Type checking (strict) | `mypy backend/` |
| **pytest** | Testing (≥60% coverage) | `pytest backend/tests/` |

### Frontend (TypeScript)

| Tool | Purpose | Command |
|------|---------|---------|
| **ESLint** | Linting | `npm run lint` |
| **Prettier** | Formatting | `npm run format` |
| **TypeScript** | Type checking | `npm run type-check` |
| **Jest** | Testing | `npm test` |

---

## Security Requirements

### JWT Flow (Phase 2 & 3)

**5-Step Security Chain:**

1. **Token Extraction**: `Authorization: Bearer <token>` header
2. **Signature Verification**: Use `BETTER_AUTH_SECRET` (HS256)
3. **Expiration Check**: Reject if expired → 401
4. **User Authorization**: Token `user_id` MUST match URL `user_id`
5. **Data Filtering**: ALWAYS filter by token `user_id` (NEVER URL user_id)

### Security Anti-Patterns

**WRONG** (Security Vulnerability):
```python
tasks = session.exec(select(Task).where(Task.user_id == user_id_from_url)).all()
```

**CORRECT** (Secure):
```python
tasks = session.exec(select(Task).where(Task.user_id == current_user['user_id'])).all()
```

### Critical Security Checklist

- [ ] JWT verification on ALL protected endpoints
- [ ] Token user_id matches URL user_id check present
- [ ] Database queries filter by token user_id (NEVER URL user_id)
- [ ] No hardcoded BETTER_AUTH_SECRET
- [ ] Proper 401 vs 403 error responses
- [ ] CORS configuration allows only frontend origin
- [ ] No SQL injection vulnerabilities (use SQLModel)

---

## Cloud-Native Requirements (Phase 3)

### Health Check Endpoints (Mandatory)

```python
@app.get("/health")
async def health_check():
    """Liveness probe - is the process running?"""
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    """Readiness probe - is the app ready to handle traffic?"""
    # Must verify DB connection
    return {"status": "ready"}
```

### Port Binding

**MUST bind to 0.0.0.0 (not 127.0.0.1):**

```python
uvicorn.run("main:app", host="0.0.0.0", port=8000)
```

### Graceful Shutdown

Handle SIGTERM/SIGINT for Kubernetes:

```python
signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigint)
```

### Structured JSON Logging

```python
import json

logger.info(json.dumps({
    "event": "mcp_tool_invoked",
    "tool": "add_task",
    "user_id": user_id[:8] + "***",  # PII protected
    "execution_time_ms": 45,
    "status": "success"
}))
```

---

## User Isolation (CRITICAL)

**EVERY database query MUST filter by user_id:**

```python
# CORRECT - Secure user isolation
tasks = session.exec(
    select(Task).where(Task.user_id == token_user_id)
).all()

# FORBIDDEN - Data leak vulnerability
tasks = session.exec(select(Task)).all()
```

---

## Quick Reference

### Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port in use | `Stop-Process -Id (Get-Process -Id <port>).Id -Force` |
| Next.js lock | `rm -f frontend-web/.next/dev/lock` |
| Module not found | `npm install --legacy-peer-deps` |
| Windows encoding | UTF-8 forcing in logger.py |

### Verification Checklist

- [ ] Backend health: http://localhost:8000/health → `{"status":"healthy"}`
- [ ] Backend docs: http://localhost:8000/docs → Swagger UI loads
- [ ] Frontend web: http://localhost:3000 → Landing page shows
- [ ] Chatbot UI: http://localhost:3001 → Chat interface loads

### Forbidden Practices

1. Never store state in module-level variables (defeats stateless design)
2. Never bypass MCP tools for direct DB access from agent
3. Never manually write production code (violates Phase 3 principle)
4. Never use `eval()` or `exec()` on user input
5. Never commit `.env` files
6. Never cache conversation state in memory
7. Never bind to 127.0.0.1 (use 0.0.0.0 for containers)
8. Never log sensitive data (API keys, user messages)

---

## References

| Resource | Path |
|----------|------|
| Phase 1 Constitution | `.specify/memory/constitution.md` |
| Phase 2 Constitution | `.specify/memory/phase-2-constitution.md` |
| Phase 3 Constitution | `.specify/memory/phase-3-constitution.md` |
| Agent Configuration | `.spec-kit/agents.yaml` |
| Project Config | `.spec-kit/config.yaml` |
| Auth Skill | `.spec-kit/skills/auth_integration.md` |
| Specs Directory | `specs/` |

---

**Last Updated**: 2025-12-31
**Maintained By**: Claude Code
