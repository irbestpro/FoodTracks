Real-Time Task Board System (FastAPI + React Native)

A real-time collaborative task/board management system with two parallel implementations:

Quick-Win Version – In-memory, simple, no authentication

State-of-the-Art Version – Production-grade using PostgreSQL, Redis Streams, WebSockets, JWT

Both versions can run independently under separate API routes.

Table of Contents

Project Overview

Architecture

Models Layer

Repository Layer

Data Layer

Utilities Layer

Controllers

Backend / Frontend Interaction

Quick-Win Architecture

Features

Example Quick-Win Board JSON

State-of-the-Art Architecture

Authentication Workflow

Redis + WebSocket Core

Advantages

How to Run

Final Notes

Project Overview

This project is built using:

FastAPI (Python) for the backend

React Native for the frontend

Redis Streams for real-time event processing

PostgreSQL for data persistence in the State-of-the-Art implementation

Pydantic for model validation and serialization

The system provides real-time task updates, event logging, authentication, and scalable architecture.

Architecture

The backend follows a multi-layer design.

Models Layer

Contains business entities such as:

Users

Boards

Tasks

Relationships

Each user owns one or more boards

Each board contains multiple tasks

Tasks are created/updated by users

Py_Models

Located in the Py_Models folder, used for:

Input validation

JSON serialization

Communication with the frontend

Compatibility with FastAPI

These classes inherit from Pydantic.

Repository Layer

Encapsulates data-handling logic:

Boards_Rep → board creation, updates, queries

Users_Rep → registration, login, authentication

This layer isolates business logic from storage details.

Data Layer

Consists of three main modules:

DB_Context

Handles PostgreSQL connections and transactions.

Quick_Win

Stores all data in memory for rapid testing.
No persistence is used.
Clears on server restart.

Redis_DB

Used in the State-of-the-Art version for:

Fast caching

Task storage

Event handling

Redis Streams for real-time updates

Utilities Layer

Contains:

WebSocket classes for real-time broadcasting

JWT helper functions

Pydantic-based configuration loader

Environment variable readers for Redis/PostgreSQL/JWT

Configuration values are securely stored in:

.env

.db.env

.jwt.env

Controllers

Two groups of controllers:

Public Controllers

Registration

Authentication

Token issuance

Protected Controllers

Require JWT validation:

Quick_Win_Boards_Route

State_Of_Art_Boards_Route

This setup allows running two independent implementations in parallel.

Backend / Frontend Interaction

All APIs use REST

CORS enables communication with the React Native app

Frontend requests use fetch()

URLs stored in Request.js

UI states controlled using useState and useEffect

Frontend modules include:

Login

Request Manager

Boards

Tasks

Messages (WebSocket-based)

Quick-Win Architecture

A simple, fast implementation suitable for demos and rapid development.

Quick-Win Features

Data stored entirely in memory

No authentication

Pydantic used for tasks

Real-time broadcast of updates using WebSockets

Server restart resets all data

Example Quick-Win Board JSON
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

State-of-the-Art Architecture

A scalable and production-ready version using Redis Streams and PostgreSQL.

Authentication Workflow

User registers.

A JWT token (containing username + ID) is generated.

Token expiration: 1 month.

Token stored automatically in browser cookies.

Every request includes the token.

TokenChecker.py validates token:

Expired → return 401, clear cookie, redirect to login

Invalid → same as above

Secret keys stored in .jwt.env.

Redis + WebSocket Core

Redis Streams handle:

Real-time synchronization

Event logging

Per-board streams

Broadcasting updates to active clients

Every task mutation generates a new Stream event.

Advantages
1. Board Isolation

Each board uses a separate Redis Stream.
Access can be restricted via tokens.

2. Event-Driven Architecture

Every action is logged as a discrete event for monitoring, scalability, and analytics.

3. Hybrid Storage

Redis for speed
PostgreSQL for persistence
Ensures sustainability across restarts.

4. Horizontal Scaling

Redis consumer groups enable multi-server deployments (Docker/Kubernetes).

5. Real-Time Monitoring

User actions can be visualized or stored for analysis.

6. Dynamic Task Fields

Both Redis and PostgreSQL support flexible schemas.

How to Run
1. Run the startup script
./Run.sh


This script launches:

FastAPI backend

React Native frontend

2. Configure Environment Variables

Before running, ensure:

.db.env

Contains PostgreSQL:

Username

Password

Host

Port

Database

.env

Contains Redis:

Host

Port

Password (optional)

.jwt.env

Contains:

JWT secret key

Hashing algorithm

Final Notes

Quick-Win → ideal for prototypes

State-of-the-Art → ideal for production

Built for real-time collaboration

Uses Redis Streams for ultra-fast updates

Both implementations run in parallel
