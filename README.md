# Real-Time To-Do List

**Full-stack Task Management System** using **FastAPI** for the backend and **React Native** for the frontend. The project supports two implementations: **Quick-Win** (in-memory storage) and **State-of-the-Art** (PostgreSQL + Redis + WebSocket).

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
- `DB_Context` – PostgreSQL connection.  
- `Quick_Win` – in-memory data storage.  
- `Redis_DB` – Redis storage for real-time events.  

### Utilities
- `WebSocketClass` – manage WebSocket connections.  
- Database configurations and JWT token settings via `.env` and Pydantic.  

### Controllers
- **Public Access**: Endpoints without login (`main.py`).  
- **Protected**: Require authentication.  
  - `Quick_Win_Boards_Route` – Quick-Win endpoints.  
  - `State_Of_Art_Boards_Route` – State-of-the-Art endpoints.  

---

## Backend / Frontend Integration
- RESTful APIs; some endpoints are asynchronous.  
- CORS middleware allows frontend access (port 3000 by default).  
- React Native frontend uses `fetch()` requests stored in `Request.js`.  
- Components: `Login`, `Request`, `Board`, `Tasks`, `Messages`.  

---

## Quick-Win Implementation
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
- Middleware (`TokenChecker.py`) validates tokens.  
- Invalid/expired tokens return `401 Unauthorized`.  
- JWT signing key loaded from `.jwt.env`.  

### Redis + WebSocket Architecture
- Redis stores tasks in memory and acts as **event bus**.  
- Each task action generates a Redis stream event.  
- Events broadcast to active clients via WebSockets.  
- Supports real-time collaboration, full event history, and low-latency updates.  

### Advantages
1. **Board Isolation** – Redis stream keys isolate boards; supports consumer groups and permissions.  
2. **Event-Driven Architecture** – Track all task events; allows real-time updates and auditing.  
3. **Caching + Persistence** – Redis for fast access, PostgreSQL for durability.  
4. **Horizontal Scaling** – Multiple backend instances supported via Redis streams.  
5. **Real-Time Monitoring** – Full event logs per board.  
6. **Flexible Task Fields** – Optional and dynamic task fields supported by Redis (ReJSON) and PostgreSQL.  

---

## How to Run
1. Run startup script:
```bash
./Run.sh
