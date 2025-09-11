import sqlite3
from datetime import datetime
from typing import List, Optional
from models import TodoCreate, TodoUpdate

class TodoDatabase:
    def __init__(self, db_name: str = "todos.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Create the todos table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_todo(self, todo: TodoCreate) -> dict:
        """Create a new todo item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO todos (title, description, due_date, created_at)
            VALUES (?, ?, ?, ?)
        ''', (todo.title, todo.description, todo.due_date, created_at))
        
        todo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return self.get_todo_by_id(todo_id)
    
    def get_all_todos(self) -> List[dict]:
        """Get all todo items"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This makes results dict-like
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
        todos = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return todos
    
    def get_todo_by_id(self, todo_id: int) -> Optional[dict]:
        """Get a specific todo by ID"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        todo = cursor.fetchone()
        
        conn.close()
        return dict(todo) if todo else None
    
    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[dict]:
        """Update a todo item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        values = []
        
        if todo_update.title is not None:
            update_fields.append("title = ?")
            values.append(todo_update.title)
        
        if todo_update.description is not None:
            update_fields.append("description = ?")
            values.append(todo_update.description)
        
        if todo_update.due_date is not None:
            update_fields.append("due_date = ?")
            values.append(todo_update.due_date)
        
        if todo_update.completed is not None:
            update_fields.append("completed = ?")
            values.append(todo_update.completed)
        
        if not update_fields:
            conn.close()
            return self.get_todo_by_id(todo_id)
        
        values.append(todo_id)
        query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return self.get_todo_by_id(todo_id)
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
