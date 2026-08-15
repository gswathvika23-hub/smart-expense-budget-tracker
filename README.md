# Smart Expense & Budget Tracker with AI Categorization

A full-stack web application for tracking personal expenses, managing category budgets, and getting AI-assisted expense categorization. Built to practice end-to-end full-stack development, from database design and REST API authentication to a connected React frontend.

## Features

- **User Authentication** — Secure registration and login with JWT tokens and bcrypt password hashing
- **Expense Management** — Full CRUD (create, read, update, delete) for tracking individual expenses, with filtering support
- **Budget Tracking** — Set monthly budgets per category and see real-time spent/remaining/percent-used calculations
- **AI-Assisted Categorization** — Suggests an expense category (Food, Travel, Shopping, Bills) based on the expense description using keyword matching
- **Interactive Dashboard** — Visual breakdown of spending by category (pie chart), budget status table, and a recent expenses feed

## Tech Stack

**Backend:** Python, FastAPI, PostgreSQL, SQLAlchemy, JWT (python-jose), Passlib (bcrypt)
**Frontend:** React (Vite), React Router, Axios, Recharts
**Tools:** Postman/Swagger UI for API testing, Git & GitHub for version control

## Architecture

- RESTful API design with protected routes using JWT bearer tokens
- CORS-enabled backend to support cross-origin requests from the React frontend
- Relational database schema with four core tables: `users`, `categories`, `expenses`, `budgets`

## API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/register` | POST | Create a new user account |
| `/token` | POST | Log in and receive a JWT access token |
| `/expenses` | GET/POST | List or create expenses |
| `/expenses/{id}` | PUT/DELETE | Update or delete an expense |
| `/budgets/` | GET/POST | List or create budgets |
| `/budgets/status` | GET | Get spent/remaining/percent-used per budget |
| `/categorize/suggest` | POST | Get an AI-suggested category for an expense description |

## Getting Started

### Backend
\`\`\`bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`
API docs available at `http://127.0.0.1:8000/docs`

### Frontend
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
App available at `http://localhost:5173`

## Roadmap

- [ ] AWS deployment (EC2, RDS, S3)
- [ ] Docker containerization
- [ ] Automated tests
- [ ] Full documentation with ER diagrams

## Screenshots

_(Add dashboard and login screenshots here)_