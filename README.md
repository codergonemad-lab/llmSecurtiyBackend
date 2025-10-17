# SecureLLM Backend

A FastAPI-based backend application for the SecureLLM platform.

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── run_dev.py             # Development server startup script
├── api/                   # API routes and endpoints
│   ├── __init__.py
│   ├── routes.py          # Main router configuration
│   └── endpoints/         # Individual endpoint modules
│       ├── __init__.py
│       ├── auth.py        # Authentication endpoints
│       ├── users.py       # User management endpoints
│       └── challenges.py  # Challenge-related endpoints
├── schema/                # Pydantic schemas for request/response
│   ├── __init__.py
│   ├── user.py           # User schemas
│   ├── auth.py           # Authentication schemas
│   └── challenge.py      # Challenge schemas
├── database/              # Database configuration and models
│   ├── __init__.py
│   ├── connection.py     # Database connection setup
│   ├── models.py         # SQLAlchemy models
│   └── init_db.py        # Database initialization script
└── utils/                 # Utility functions and helpers
    ├── __init__.py
    ├── auth.py           # Authentication utilities
    ├── security.py       # Security-related utilities
    └── challenges.py     # Challenge-related utilities
```

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   copy .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:

   ```bash
   python database/init_db.py
   ```

5. Run the development server:
   ```bash
   python run_dev.py
   ```

## API Documentation

Once the server is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Features

- JWT-based authentication
- User management
- Challenge system
- Progress tracking
- RESTful API design
- Auto-generated documentation
- Database models with relationships
- Security utilities
- CORS support for frontend integration

## Development

The application uses:

- **FastAPI** for the web framework
- **SQLAlchemy** for ORM
- **Pydantic** for data validation
- **JWT** for authentication
- **Uvicorn** for ASGI server
- **PostgreSQL/SQLite** for database
