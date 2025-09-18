# Todo List Manager - DevOps Class Project

A full-stack todo list application built with FastAPI (Python) backend and vanilla JavaScript frontend, designed for DevOps pipeline implementation.

## Features

- Create new todo items with title, description, and due date
- View all todos in an organized, responsive interface
- Mark todos as complete/incomplete with visual feedback
- Delete todos with confirmation dialog
- Persistent storage using SQLite database
- RESTful API with automatic documentation
- Responsive design for mobile and desktop

## Tech Stack

### Backend
- **Python 3.8+** - Programming language
- **FastAPI** - Modern web framework for building APIs
- **SQLite** - Lightweight relational database
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for running the application

### Frontend
- **HTML5** - Structure and semantic markup
- **CSS3** - Styling with modern features
- **Vanilla JavaScript** - Client-side functionality and API communication

## Project Structure
todo-devops-app/
├── backend/
│   ├── main.py          # FastAPI application and API routes
│   ├── database.py      # Database operations and CRUD functions
│   ├── models.py        # Pydantic models for data validation
│   └── todos.db         # SQLite database (created automatically)
├── frontend/
│   ├── index.html       # Main HTML interface
│   ├── style.css        # CSS styling and responsive design
│   └── script.js        # JavaScript functionality and API calls
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This documentation
## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git for version control

### Quick Start

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd todo-devops-app
