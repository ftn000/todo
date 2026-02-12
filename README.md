# TODO Manager (FastAPI)

A task management web application built with **FastAPI** following **Clean Architecture principles**.

The project demonstrates separation of concerns, dependency injection, and isolation of business logic from infrastructure.

---

## Features

- Create and delete tasks
- Mark tasks as completed
- Daily tasks with streak counter
- Automatic daily reset (once per day)
- Focus of the Day (only one task per day)
- Task grouping:
  - Daily
  - Active
  - Future
  - Overdue
  - Done

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Jinja2 (server-side rendering)
- Dependency Injection (FastAPI `Depends`)

---

##  Architecture

The project follows **Clean Architecture** principles.

### Layered Structure

```tex
Client → API → Services → Repositories → Database
Layer Responsibilities
API
Handles HTTP requests

Contains no business logic

Uses Dependency Injection

Converts DomainError into HTTP responses

Services
Contains all business rules and application logic:

TaskService — task management

FocusService — focus-of-the-day logic

DailyService — daily reset logic

Business rules implemented here:

A completed task cannot become focus

Only one focus task per day

Daily tasks reset once per day

Domain
Task model

DomainError exceptions

Repository interfaces (TaskRepository, MetaRepository)

The Domain layer does not depend on FastAPI or SQLAlchemy.

Infrastructure
SQLAlchemy ORM implementation

SQLite database

Alternative JSON repository implementation

Infrastructure can be replaced without changing business logic.
```
Project Structure
```
app/
├── api/
├── domain/
├── infrastructure/
├── services/
└── utils/
```
How to Run
```
git clone <repo-url>
cd todo
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python start.py
```
Application will be available at:
```
http://127.0.0.1:8000
```
Future Improvements
```
User authentication

Multi-user support

REST API (JSON endpoints)

Alembic migrations

Docker support

Unit tests for services
```
Purpose of the Project
This project was created to practice backend architecture design, dependency injection, and clean separation between business logic and infrastructure.

