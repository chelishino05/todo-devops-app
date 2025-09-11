// API base URL
const API_BASE_URL = 'http://localhost:8000/api';

// DOM elements
const todoForm = document.getElementById('todoForm');
const todoList = document.getElementById('todoList');
const loadingMessage = document.getElementById('loadingMessage');
const errorMessage = document.getElementById('errorMessage');
const emptyMessage = document.getElementById('emptyMessage');
const notification = document.getElementById('notification');

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadTodos();
    setupFormSubmission();
});

// Load all todos from backend
async function loadTodos() {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch(`${API_BASE_URL}/todos`);
        
        if (!response.ok) {
            throw new Error(`Failed to load todos: ${response.status}`);
        }
        
        const todos = await response.json();
        displayTodos(todos);
        
    } catch (error) {
        console.error('Error loading todos:', error);
        showError('Failed to load todos. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Display todos in the UI
function displayTodos(todos) {
    if (todos.length === 0) {
        todoList.innerHTML = '';
        emptyMessage.style.display = 'block';
        return;
    }
    
    emptyMessage.style.display = 'none';
    
    todoList.innerHTML = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
            <div class="todo-header">
                <h3 class="todo-title">${escapeHtml(todo.title)}</h3>
                <span class="todo-status">${todo.completed ? 'Completed' : 'Pending'}</span>
            </div>
            
            ${todo.description ? `<div class="todo-description">${escapeHtml(todo.description)}</div>` : ''}
            
            <div class="todo-meta">
                <div class="todo-dates">
                    <div>Created: ${formatDate(todo.created_at)}</div>
                    ${todo.due_date ? `<div class="todo-due-date">Due: ${formatDate(todo.due_date)}</div>` : ''}
                </div>
                
                <div class="todo-actions">
                    ${!todo.completed ? `
                        <button class="btn-secondary" onclick="toggleTodoComplete(${todo.id}, true)">
                            Mark Complete
                        </button>
                    ` : `
                        <button class="btn-secondary" onclick="toggleTodoComplete(${todo.id}, false)">
                            Mark Incomplete
                        </button>
                    `}
                    <button class="btn-danger" onclick="deleteTodo(${todo.id})">
                        Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Setup form submission
function setupFormSubmission() {
    todoForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(todoForm);
        const todoData = {
            title: formData.get('title').trim(),
            description: formData.get('description').trim() || null,
            due_date: formData.get('due_date') || null
        };
        
        if (!todoData.title) {
            showNotification('Title is required', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/todos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(todoData)
            });
            
            if (!response.ok) {
                throw new Error(`Failed to create todo: ${response.status}`);
            }
            
            await response.json();
            
            todoForm.reset();
            showNotification('Todo created successfully!', 'success');
            loadTodos();
            
        } catch (error) {
            console.error('Error creating todo:', error);
            showNotification('Failed to create todo. Please try again.', 'error');
        }
    });
}

// Toggle todo completion
async function toggleTodoComplete(todoId, completed) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to update todo: ${response.status}`);
        }
        
        showNotification(
            completed ? 'Todo marked as complete!' : 'Todo marked as incomplete!', 
            'success'
        );
        loadTodos();
        
    } catch (error) {
        console.error('Error updating todo:', error);
        showNotification('Failed to update todo. Please try again.', 'error');
    }
}

// Delete a todo
async function deleteTodo(todoId) {
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`Failed to delete todo: ${response.status}`);
        }
        
        showNotification('Todo deleted successfully!', 'success');
        loadTodos();
        
    } catch (error) {
        console.error('Error deleting todo:', error);
        showNotification('Failed to delete todo. Please try again.', 'error');
    }
}

// Helper functions
function showLoading(show) {
    loadingMessage.style.display = show ? 'block' : 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function showNotification(message, type = 'success') {
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';
    
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
