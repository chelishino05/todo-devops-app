"""
Database layer for Todo application
Handles all database operations with proper connection management and error handling
"""

import sqlite3
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from models import TodoCreate, TodoUpdate
from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass


class TodoDatabase:
    """
    Database handler for Todo items
    Implements proper connection management and CRUD operations
    """
    
    def __init__(self, db_name: Optional[str] = None):
        """Initialize database with configurable name"""
        self.db_name = db_name or settings.database_name
        self.init_db()
        logger.info(f"Database initialized: {self.db_name}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Ensures proper connection handling and cleanup
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
    
    def init_db(self) -> None:
        """Create the todos table if it doesn't exist"""
        try:
            with self.get_connection() as conn:
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
                logger.info("Database tables initialized successfully")
        except DatabaseError as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def create_todo(self, todo: TodoCreate) -> Dict[str, Any]:
        """Create a new todo item"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                created_at = datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT INTO todos (title, description, due_date, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (todo.title, todo.description, todo.due_date, created_at))
                
                todo_id = cursor.lastrowid
                logger.info(f"Created todo with id: {todo_id}")
                
            return self.get_todo_by_id(todo_id)
        except DatabaseError as e:
            logger.error(f"Failed to create todo: {e}")
            raise
    
    def get_all_todos(self) -> List[Dict[str, Any]]:
        """Get all todo items"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
                todos = [dict(row) for row in cursor.fetchall()]
                logger.info(f"Retrieved {len(todos)} todos")
                return todos
        except DatabaseError as e:
            logger.error(f"Failed to retrieve todos: {e}")
            raise
    
    def get_todo_by_id(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific todo by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
                todo = cursor.fetchone()
                
                if todo:
                    logger.info(f"Retrieved todo with id: {todo_id}")
                    return dict(todo)
                else:
                    logger.warning(f"Todo not found with id: {todo_id}")
                    return None
        except DatabaseError as e:
            logger.error(f"Failed to retrieve todo {todo_id}: {e}")
            raise
    
    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[Dict[str, Any]]:
        """Update a todo item"""
        try:
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
                logger.info(f"No fields to update for todo {todo_id}")
                return self.get_todo_by_id(todo_id)
            
            values.append(todo_id)
            query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                
                if cursor.rowcount == 0:
                    logger.warning(f"Todo not found for update: {todo_id}")
                    return None
                
                logger.info(f"Updated todo with id: {todo_id}")
            
            return self.get_todo_by_id(todo_id)
        except DatabaseError as e:
            logger.error(f"Failed to update todo {todo_id}: {e}")
            raise
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
                deleted = cursor.rowcount > 0
                
                if deleted:
                    logger.info(f"Deleted todo with id: {todo_id}")
                else:
                    logger.warning(f"Todo not found for deletion: {todo_id}")
                
                return deleted
        except DatabaseError as e:
            logger.error(f"Failed to delete todo {todo_id}: {e}")
            raise
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about todos"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT COUNT(*) as total FROM todos')
                total = cursor.fetchone()['total']
                
                cursor.execute('SELECT COUNT(*) as completed FROM todos WHERE completed = 1')
                completed = cursor.fetchone()['completed']
                
                return {
                    'total': total,
                    'completed': completed,
                    'pending': total - completed
                }
        except DatabaseError as e:
            logger.error(f"Failed to get stats: {e}")
            raise