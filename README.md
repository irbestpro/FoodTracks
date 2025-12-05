# Real-Time Task Board System
FastAPI (Python) • React Native • Redis Streams • PostgreSQL

A real-time collaborative task and board management system supporting two architectures:

- **Quick-Win**: Lightweight, in-memory, no authentication  
- **State-of-the-Art**: Production-ready, scalable, with JWT authentication, Redis Streams, PostgreSQL persistence


## Table of Contents
1. Overview  
2. Architecture  
3. Backend Layers  
4. Frontend Integration  
5. Quick-Win Architecture  
6. State-of-the-Art Architecture  
7. Advantages  
8. Example JSON  
9. How to Run  
10. Final Notes  


# Overview
This project provides a real-time Kanban-style task board.  
The backend is built with **FastAPI**, **Redis**, and **PostgreSQL**, while the frontend uses **React Native**.

Two implementations exist:

| Version | Purpose |
|--------|---------|
| Quick-Win | Simple & fast prototype using in-memory storage |
| State-of-the-Art | Full scalable production system with streaming, JWT, monitoring |



# Architecture
The backend is structured cleanly in multiple layers:

- **Models Layer** – Domain and Pydantic models  
- **Repository Layer** – Business logic and interactions  
- **Data Layer** – Redis, PostgreSQL, and memory-based Quick-Win mode  
- **Utilities** – WebSocket manager, JWT tools, settings loader  
- **Controllers (Routes)** – REST API endpoints for both architecture versions  


## Models Layer
Includes the following domain entities:

- User  
- Board  
- Task  

Also includes `Py_Models/` (Pydantic models) used for validation and serialization.


## Repository Layer
Responsible for implementing operations such as:

- Creating boards  
- Adding or updating tasks  
- User operations (login, token creation, validation)  


## Data Layer

### DB_Context  
Manages PostgreSQL connections and persistent queries.

### Quick_Win  
An in-memory implementation that stores all data without databases.

### Redis_DB  
Handles:
- Redis JSON storage  
- Redis Streams event bus  
- Real-time updates over WebSocket  


## Utilities
Includes support tools:

- JWT token creation & validation  
- WebSocket connection manager  
- `.env` configuration system  
- TokenChecker for request authentication  


## Controllers
There are two levels of routing:

- **Public routes** (login, register)  
- **Protected routes** for Quick-Win and State-of-the-Art  
  - `Quick_Win_Boards_Route`  
  - `State_Of_Art_Boards_Route`  


# Frontend Integration
The frontend communicates using REST API + WebSocket.

- API endpoints are stored in `Utilities/Request.js`  
- React Native uses `useState` and `useEffect`  
- CORS configured for local development  

Core UI components:
- Login  
- Boards  
- Tasks  
- Real-time messages  


# Quick-Win Architecture
A simple, rapid prototype with:

- No authentication  
- All boards & tasks stored in memory  
- Pydantic models for validation  
- WebSocket for instant board updates  
- No persistence (data resets when server restarts)  


## Quick-Win Features
- Very fast development  
- Real-time task updates  
- No database dependency  
- Minimal configuration required  


# State-of-the-Art Architecture
A full production-level architecture.

## Authentication Flow
1. User registers  
2. Server generates a JWT containing username + user_id  
3. Token valid for **1 month**  
4. Token stored in browser cookies  
5. Every request automatically includes the cookie  
6. `TokenChecker.py` validates the token  
7. Invalid/expired token → return **401**, clear cookie, redirect to login  
8. JWT secrets stored in `.jwt.env`  


## Redis + WebSocket Core
Redis Streams function as the **event bus**:

- Every Add/Update/Delete on a task creates an event  
- Events are sent instantly to all connected WebSocket clients  
- All events are stored and retrievable as history  


# Advantages

## 1. Board Isolation via Redis Streams
Each board has its own stream → isolated events & consumer groups.

## 2. Event-Driven Architecture
Allows:
- Monitoring  
- Logging  
- Analytics  
- Real-time dashboards  

## 3. Hybrid Storage (Redis + PostgreSQL)
- Redis = Fast caching + streaming  
- PostgreSQL = Durability & long-term persistence  

## 4. Horizontal Scaling
Redis supports unlimited backend instances.

## 5. Real-Time Monitoring
Admin can track every action immediately.

## 6. Dynamic Task Structure
Using Redis ReJSON + PostgreSQL flexible fields.


# Example JSON (Quick-Win)

```json
{
  "boards": [
    {
      "id": 1,
      "name": "Project Alpha",
      "tasks": [
        {
          "id": 1,
          "title": "Set up repository",
          "description": "Initialize GitHub repo and configure CI/CD",
          "status": "finished",
          "created_at": "2025-12-01T09:00:00",
          "updated_at": "2025-12-01T12:00:00",
          "assigned_to": "user_1"
        }
      ],
      "events": [
        {
          "action": "Add",
          "task": {
            "id": 1,
            "title": "Set up repository",
            "status": "finished",
            "created_at": "2025-12-01T09:00:00"
          },
          "timestamp": "2025-12-01T09:00:00"
        }
      ]
    }
  ]
}
