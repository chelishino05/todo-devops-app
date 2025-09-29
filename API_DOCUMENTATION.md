# API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### Health Check
- **GET** `/api/health`
- **Description**: Check if the API is running
- **Response**: `{"status": "healthy"}`

### Get All Todos
- **GET** `/api/todos`
- **Description**: Retrieve all todo items
- **Response**: Array of todo objects

### Create Todo
- **POST** `/api/todos`
- **Description**: Create a new todo item
- **Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "due_date": "YYYY-MM-DD (optional)"
}
