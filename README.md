# Real-Time To-Do List

**Full-stack Task Management System** using **FastAPI** for the backend (Python 3.11.x) and **React Native** for the frontend. The project supports two implementations: **Quick-Win** (in-memory storage) and **State-of-the-Art** (PostgreSQL + Redis + WebSocket).

---

## Table of Contents
- [Project Overview](#project-overview)  
- [Architecture](#architecture)  
  - [Models Layer](#models-layer)  
  - [Repository Layer](#repository-layer)  
  - [Data Layer](#data-layer)  
  - [Utilities](#utilities)  
  - [Controllers](#controllers)  
- [Backend / Frontend Integration](#backend--frontend-integration)  
- [Quick-Win Implementation](#quick-win-implementation)  
- [State-of-the-Art Architecture](#state-of-the-art-architecture)  
  - [Authentication](#authentication)  
  - [Redis + WebSocket Architecture](#redis--websocket-architecture)  
  - [Advantages](#advantages)  
- [How to Run](#how-to-run)  
- [Environment Variables](#environment-variables)  

---

## Project Overview
This project provides a collaborative task management system with multiple boards and tasks. Users can create boards, add tasks, and track task events in real time.  

Two implementations exist:

1. **Quick-Win** – stores all data in memory (no persistence).  
2. **State-of-the-Art** – uses PostgreSQL for persistence, Redis for caching & streaming, and WebSockets for real-time updates.

---

## Architecture

### Models Layer
- **Classes**: `Users`, `Boards`, `Tasks`.  
- **Relationships**:  
  - Each user can create one or more boards.  
  - Each board can have multiple tasks.  
  - Each task is created or updated by a user.  
- **Persistence**: Handled in PostgreSQL (State-of-the-Art).  
- **Py_Models**: Pydantic-based classes for data validation and JSON serialization.  

### Repository Layer
- `Boards_Rep` – manage boards (add, fetch).  
- `Users_Rep` – handle registration, login, authentication.  

### Data Layer
- `DB_Context` – PostgreSQL connection (Using alembic and SQLAlchemy libraries to manage the database migrations) 
- `Quick_Win` – in-memory data storage.  
- `Redis_DB` – Redis storage for real-time events.  

### Utilities
- `WebSocketClass` – manage WebSocket connections.  
- Database configurations and JWT token settings via `.env` and PydanticSetting.  

### Controllers
- **Public Access**: Endpoints without login (`main.py`).  
- **Protected**: Require authentication.  
  - `Quick_Win_Boards_Route` – Quick-Win endpoints.  
  - `State_Of_Art_Boards_Route` – State-of-the-Art endpoints.  

---

## Backend / Frontend Integration
- The system exposes RESTful APIs, with some endpoints implemented asynchronously to ensure proper concurrency when handling task operations. Two separate API route groups are available:

- **Quick Win Boards Route**  
  All endpoints are prefixed with:  
  `/api/qw/boards`

- **State-of-the-Art Boards Route**  
  All endpoints are prefixed with:  
  `/api/boards`

- CORS middleware allows frontend access (port 3000 by default).  
- React Native frontend uses `fetch()` requests stored in `Request.js` (for post and get requests).
- Components: `Login`, `Request`, `Board`, `Tasks`, `Messages` (Each component has it's own callback, effect and state to handle different conditions of transferred tasks).

---

## Quick-Win Implementation
The Quick Win perspective uses a fully in-memory architecture built on Python dictionaries and FastAPI WebSockets. Boards, tasks, and event streams are stored in nested dictionaries, providing instant reads/writes and lightweight real-time updates. A Redis-like event stream is simulated with list append operations, and a background streamer coroutine broadcasts new events to WebSocket clients. This approach prioritizes speed, simplicity, and low setup cost—ideal for prototyping and small-scale usage. The basic features of this perspective are:

- No authentication required.  
- Boards stored as in-memory lists of dictionaries.  
- Tasks represented as Pydantic objects.  
- All changes broadcast via WebSockets.  
- Data is **not persisted**; restarting the server clears all data.  

---

## State-of-the-Art Architecture

### Authentication
- Users register and login to get a **JWT token** (1-month expiration).  
- Tokens stored securely in browser cookies.  
- Middleware (`TokenChecker.py`) validates tokens per each request.  
- Invalid/expired tokens return `401 Unauthorized`.  
- JWT signing key loaded from `.jwt.env`.  

### Redis + WebSocket Architecture
- Redis stores tasks in memory and acts as **event bus** (Redis Streams).  
- Each task action generates a Redis stream event.  
- Events broadcast to active clients via WebSockets.  
- Supports real-time collaboration, full event history, and low-latency updates.  

### Advantages
1. **Board Isolation** – Redis stream keys isolate boards; supports consumer groups and permissions.  
2. **Event-Driven Architecture** – Track all task events; allows real-time updates and auditing.  
3. **Caching + Persistence** – Redis for fast access, PostgreSQL for durability.  
4. **Horizontal Scaling** – Multiple backend instances supported via Redis streams group (Each group runs on a worker with some consumers).  
5. **Real-Time Monitoring** – Full event logs per board.  
6. **Flexible Task Fields** – Optional and dynamic task fields supported by Redis (ReJSON) and PostgreSQL.  
7. **Extensibility** – The event-driven design, flexible schema (ReJSON + Postgres), and webhook integration enable new services, workflows, and UI components to be added without modifying core logic. Extensions simply subscribe to board events, attach custom automation rules, or add new task metadata, making the platform easy to evolve for future requirements.

---

## How to Run
1. Run startup script:
```bash
./Run.sh

2. Run docker-compose.yml file:
```docker-compose up --build
