# 🚀 Lead Management CRM with AI Assistant

A robust, asynchronous microservice built with FastAPI for managing leads and transferring them to the sales department using an AI-powered scoring system.

## 🛠 Tech Stack
* **Framework:** FastAPI (Python 3.11)
* **Database:** PostgreSQL + `asyncpg`
* **ORM:** SQLAlchemy (Async)
* **Configuration:** Pydantic V2 (`pydantic-settings` with computed fields)
* **Infrastructure:** Docker & Docker Compose (with DB healthchecks)

---

## 🚦 Quick Start

The application is fully containerized and ready to run out of the box.

1. Clone the repository and navigate to the project root.
2. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
3. Once the database is initialized and the API is running, access the interactive Swagger UI documentation at:
   ```http://localhost:8000/docs```

## How the system works
The system is built on a Layered Architecture strictly following SOLID principles:

- API Layer (Routers): Handles HTTP requests, responses, and payload validation via Pydantic.

- Service Layer: Encapsulates the core business logic. It implements a State Machine using an ALLOWED_TRANSITIONS mapping to strictly enforce the lead lifecycle (preventing stage skipping or modification of protected states like transferred).

- Data Layer: Handles asynchronous database operations using SQLAlchemy.

- Dependency Injection: Database sessions and the AI Service are injected into controllers using FastAPI's Depends, ensuring loose coupling and testability.

## Where AI is used and why
AI is utilized during the lead qualification phase ```POST /leads/{lead_id}/analyze```.

**Why**: Sales teams often waste resources nurturing "cold" leads. The AI acts as a smart advisor, instantly scoring a lead's probability of conversion based on objective metrics. It helps managers prioritize high-value prospects and acts as a safeguard (preventing the transfer of leads with a score < 0.6).

## What data is given to the AI
To evaluate the lead, the AI service is provided with a concise business context snapshot:

- source (Acquisition channel: scanner, partner, manual)

- stage (Current funnel stage)

- business_domain (Presence and specific type of business domain)

- activity_count (Level of engagement / communication history)

## What decisions the human makes
The system embraces a Human-in-the-Loop philosophy. The AI is an advisor, not an autonomous agent. The human manager is responsible for:

- Creating the lead and inputting initial data.

- Communicating with the client (which organically drives up the activity_count).

- Advancing the lead through the funnel (contacted ➔ qualified).

- The Final Call: Clicking the "Transfer to sales" button. The AI evaluates the constraints, but the actual command to execute the transfer is entirely human-driven.

## What I would complicate/improve in a real project
Since this is an MVP, certain features were abstracted. In a Production environment, I would implement:

- Real LLM Integration: The current AI is a rule-based heuristic model built behind a BaseAIService interface. In a real project, I would implement an OpenAIService class to analyze actual raw text from client communications using prompt engineering. The Dependency Inversion setup makes this swap seamless.

- Auth & Authorization (JWT): Implement Role-Based Access Control (RBAC) to track which specific manager (user_id) created or transferred a lead.

- Audit Logging: Introduce a separate table to log all stage transitions with timestamps for pipeline analytics (e.g., calculating time-in-stage).

- Database Migrations: Integrate Alembic for safe, version-controlled database schema updates instead of relying on Base.metadata.create_all.

- Comprehensive Testing: Add pytest to cover the State Machine logic, AI scoring edge cases, and API integration tests.

## additional - Testing the Main Flow
To successfully transfer a lead to sales, the lead must achieve an ai_score >= 0.6, have a business domain, and be in the qualified stage.

Create a strong lead: (POST /leads/)

**JSON**
``` brush
{
  "source": "partner",
  "business_domain": "first"
} 
```
Analyze the lead: (POST /leads/{lead_id}/analyze)

Because the source is 'partner' and it has a domain, the mock AI will score it >= 0.6.

Move through the funnel: (PATCH /leads/{lead_id}/stage)

Update to "contacted"

Update to "qualified"

Transfer to Sales: (POST /leads/{lead_id}/transfer)

Observe the successful 200 OK response and the creation of a new Sale record.