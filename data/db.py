# data/db.py
"""
Database handler for Task Manager
Uses SQLite3 for persistent storage with enhanced schema
"""

import sqlite3
from datetime import date, datetime
from typing import List, Optional
from task import Task


class Database:
    """Handles all database operations for tasks"""
    
    def __init__(self, db_name: str = "tasks.db"):
        """Initialize database connection and create tables if not exists"""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        self.create_table()

    # ----------------------------------------------------------------------
    # Table Setup
    # ----------------------------------------------------------------------
    def create_table(self) -> None:
        """
        Create tasks table with enhanced schema.
        Supports priority, timestamps, and proper date handling.
        """
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            description TEXT,
            due_date TEXT,              -- Stored as ISO format (YYYY-MM-DD)
            completed INTEGER NOT NULL DEFAULT 0,
            priority TEXT DEFAULT 'medium',  -- low, medium, high
            created_at TEXT NOT NULL,         -- ISO timestamp
            updated_at TEXT NOT NULL          -- ISO timestamp
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    # ----------------------------------------------------------------------
    # CRUD Operations (Create, Read, Update, Delete)
    # ----------------------------------------------------------------------
    def add_task(self, task: Task) -> bool:
        """Add a new task to database. Converts datetime objects to ISO strings."""
        query = """
        INSERT INTO tasks (title, description, due_date, completed, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.conn.execute(query, (
                task.title,
                task.description,
                task.due_date.isoformat() if task.due_date else None,
                int(task.completed),
                task.priority,
                task.created_at.isoformat(),
                task.updated_at.isoformat()
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Duplicate title

    def remove_task(self, title: str) -> bool:
        """Delete a task by its title"""
        query = "DELETE FROM tasks WHERE title = ?"
        cursor = self.conn.execute(query, (title,))
        self.conn.commit()
        return cursor.rowcount > 0

    def find_task(self, title: str) -> Optional[Task]:
        """Retrieve a single task by title"""
        query = "SELECT * FROM tasks WHERE title = ?"
        cursor = self.conn.execute(query, (title,))
        row = cursor.fetchone()
        if row:
            return self._row_to_task(row)
        return None

    def list_tasks(self, filter_by: str = "all") -> List[Task]:
        """
        Retrieve tasks with optional filtering.
        filter_by: 'all', 'completed', 'pending', 'overdue'
        """
        if filter_by == "completed":
            query = "SELECT * FROM tasks WHERE completed = 1 ORDER BY due_date ASC"
        elif filter_by == "pending":
            query = "SELECT * FROM tasks WHERE completed = 0 ORDER BY due_date ASC"
        elif filter_by == "overdue":
            today = date.today().isoformat()
            query = "SELECT * FROM tasks WHERE completed = 0 AND due_date < ? ORDER BY due_date ASC"
            cursor = self.conn.execute(query, (today,))
            rows = cursor.fetchall()
            return [self._row_to_task(row) for row in rows]
        else:  # 'all'
            query = "SELECT * FROM tasks ORDER BY completed ASC, due_date ASC"
        
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    # ----------------------------------------------------------------------
    # Update Operations
    # ----------------------------------------------------------------------
    def update_task_completion(self, title: str, completed: bool) -> bool:
        """Update task completion status and auto-update timestamp"""
        current_time = datetime.now().isoformat()
        query = "UPDATE tasks SET completed = ?, updated_at = ? WHERE title = ?"
        cursor = self.conn.execute(query, (int(completed), current_time, title))
        self.conn.commit()
        return cursor.rowcount > 0

    def update_task_priority(self, title: str, priority: str) -> bool:
        """Update task priority and refresh updated_at timestamp"""
        valid_priorities = {"low", "medium", "high"}
        if priority not in valid_priorities:
            return False
            
        current_time = datetime.now().isoformat()
        query = "UPDATE tasks SET priority = ?, updated_at = ? WHERE title = ?"
        cursor = self.conn.execute(query, (priority, current_time, title))
        self.conn.commit()
        return cursor.rowcount > 0

    def update_task_due_date(self, title: str, due_date: Optional[date]) -> bool:
        """Update task due date and refresh updated_at timestamp"""
        current_time = datetime.now().isoformat()
        due_str = due_date.isoformat() if due_date else None
        query = "UPDATE tasks SET due_date = ?, updated_at = ? WHERE title = ?"
        cursor = self.conn.execute(query, (due_str, current_time, title))
        self.conn.commit()
        return cursor.rowcount > 0

    # ----------------------------------------------------------------------
    # Utility Methods
    # ----------------------------------------------------------------------
    def get_task_count(self, completed: Optional[bool] = None) -> int:
        """Get number of tasks, optionally filtered by completion status"""
        if completed is True:
            query = "SELECT COUNT(*) FROM tasks WHERE completed = 1"
        elif completed is False:
            query = "SELECT COUNT(*) FROM tasks WHERE completed = 0"
        else:
            query = "SELECT COUNT(*) FROM tasks"
        
        cursor = self.conn.execute(query)
        return cursor.fetchone()[0]

    def delete_all_tasks(self) -> int:
        """Delete all tasks and return number of deleted rows"""
        cursor = self.conn.execute("DELETE FROM tasks")
        self.conn.commit()
        return cursor.rowcount

    # ----------------------------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------------------------
    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert database row to Task object. Parses dates and timestamps."""
        # Parse due_date from string to date object
        due_date = None
        if row["due_date"]:
            try:
                due_date = datetime.fromisoformat(row["due_date"]).date()
            except (ValueError, TypeError):
                pass
        
        # Parse timestamps
        created_at = datetime.now()
        if row["created_at"]:
            try:
                created_at = datetime.fromisoformat(row["created_at"])
            except (ValueError, TypeError):
                pass
        
        updated_at = datetime.now()
        if row["updated_at"]:
            try:
                updated_at = datetime.fromisoformat(row["updated_at"])
            except (ValueError, TypeError):
                pass
        
        # Create Task object with all fields
        task = Task(
            title=row["title"],
            description=row["description"] or "",
            due_date=due_date,
            completed=bool(row["completed"]),
            priority=row["priority"] or "medium",
            created_at=created_at,
            updated_at=updated_at
        )
        
        return task

    def close(self) -> None:
        """Close database connection safely"""
        if self.conn:
            self.conn.close()
