# 🧠 Finvest-AI

> **An AI-driven financial analytics and advisory platform built with FastAPI, Celery, Redis, and PostgreSQL.**

Finvest-AI is a modular, scalable backend framework for intelligent financial applications — enabling portfolio insights, real-time data processing, and AI-powered chat-based advisory.  
It’s designed for speed, maintainability, and modern software practices.

---

## 📁 Project Structure

```
finvest-ai/
├── .github/                # CI/CD workflows and templates
├── docker/                 # Dockerfile configurations
├── ops/                    # Makefiles, compose configs, and deployment scripts
├── src/
│   ├── api/                # FastAPI route definitions
│   ├── app/                # Application core setup and startup logic
│   ├── core/               # Settings, security, and configuration
│   ├── db/                 # Database and migration logic
│   ├── models/             # SQLModel / ORM models
│   ├── repositories/       # Data access layer
│   ├── services/           # Business logic and domain services
│   ├── schemas/            # Pydantic schemas
│   ├── workers/            # Celery background task definitions
│   └── main.py             # FastAPI application entrypoint
├── tests/                  # Pytest-based unit and integration tests
├── pyproject.toml          # Project dependencies and tool configuration
├── README.md               # Project documentation
└── Makefile                # Common project commands
```

---

## 🧠 Overview

Finvest-AI is a **financial intelligence platform** that helps users analyze portfolios, forecast gains, and interact with AI-driven advisors using conversational interfaces.  
It provides a secure, modular, and cloud-ready API backend suitable for financial analytics, investment management, or fintech automation.

---

## ⚡ Features

- 🧩 **Modular FastAPI Backend** — Clean architecture for scalable services  
- 🧠 **AI-Powered Insights** — Leverages LLMs for financial reasoning and chat-based support  
- 🏦 **Portfolio Intelligence** — Analyze asset performance, risk, and tax implications  
- 🔄 **Asynchronous Processing** — Powered by Celery + Redis  
- 🧾 **PostgreSQL + SQLModel ORM** — Efficient and type-safe database integration  
- 🐳 **Dockerized Deployment** — Seamless local and production builds  
- 🧪 **Comprehensive Testing** — Pytest setup with coverage and mocks  
- 🔐 **JWT Authentication & Role Management**  
- 📊 **Structured Logging and Monitoring**  
- 🚀 **Ready for Cloud / Microservices Architecture**

---

## ⚙️ Environment Setup

### 🐍 Python Setup

Install dependencies using [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
source .venv/bin/activate
```
### 🧰 Installing `make` on Windows (via Chocolatey)

If you don't have `make` installed on your Windows machine, you can install it using [Chocolatey](https://chocolatey.org/):

1. First, ensure you have Chocolatey installed — follow the instructions at [https://chocolatey.org/install](https://chocolatey.org/install)
2. Then install `make` by running:

```bash
choco install make
```

After installation, restart your terminal or PowerShell to ensure `make` is available in your PATH.

---

### 🐳 Docker Setup

```bash
make up         # Start containers
make down       # Stop containers
make build      # Build images
make logs       # View logs
```

### 🗃️ Database Management

```bash
make alembic-revision name="add_new_table"
make alembic-upgrade
make alembic-downgrade
```

---

## 🧱 Makefile Commands (Top-Level)

| Command | Description |
|----------|-------------|
| `make up` | Start all containers |
| `make down` | Stop containers |
| `make build` | Build all services |
| `make alembic-migrate` | Run Alembic migrations |
| `make alembic-revision` | Create a new Alembic migration |
| `make test` | Run test suite |
| `make lint` | Lint codebase using Ruff |
| `make hooks` | Setup pre-commit hooks |

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Framework** | FastAPI |
| **ORM** | SQLModel / SQLAlchemy |
| **Database** | PostgreSQL |
| **Cache / Broker** | Redis |
| **Background Jobs** | Celery |
| **Containerization** | Docker, Docker Compose |
| **Testing** | Pytest |
| **Typing & Linting** | mypy, ruff, black, isort |
| **Package Manager** | uv |

---

## 📈 API Overview

Example base route (from `src/api/v1/chat.py`):

```python
@router.post("/")
async def chat(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Create a new chat session for financial AI advisory.
    """
    user_id = request.state.user_id
    chat_repo = BaseSQLAlchemyRepository[ChatSession](db, ChatSession)
    session_data = ChatSession(user_id=user_id, title="AI Financial Session")
    new_session = await chat_repo.create(session_data)
    return {"status": "success", "session_id": new_session.id}
```

---

## 🚀 Running the App (Local Dev)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

App will be available at:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testing

```bash
pytest --cov=src
```

To run tests inside Docker:

```bash
make test
```

---

## 🧭 Roadmap

- [x] Setup base FastAPI architecture  
- [x] PostgreSQL + Redis integration  
- [x] JWT-based authentication  
- [ ] AI chat integration (LLM connector)  
- [ ] Portfolio analytics engine  
- [ ] Dashboard frontend (Vue / Next.js)  
- [ ] CI/CD pipelines  
- [ ] Public API documentation  

---

## 🙌 Acknowledgments

This project builds upon:

- FastAPI Base Template - https://github.com/GabrielVGS/fastapi-base  
- SQLModel  
- Celery  
- Docker  
- uv
