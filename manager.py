# manager.py
"""
Task Manager - Business logic layer
"""

from typing import List, Optional
from datetime import datetime, date
from task import Task
from data.db import Database


class TaskManager:
    """Main controller for task operations. Handles business logic and validation."""
    
    def __init__(self):
        """Initialize manager with database connection"""
        self.db = Database()

    # ----------------------------------------------------------------------
    # Basic CRUD Operations
    # ----------------------------------------------------------------------
    def add_task(self, task: Task) -> bool:
        """Add a new task to the system"""
        return self.db.add_task(task)

    def remove_task(self, title: str) -> bool:
        """Delete a task by its title"""
        return self.db.remove_task(title)

    def find_task(self, title: str) -> Optional[Task]:
        """Search for a task by title"""
        return self.db.find_task(title)

    # ----------------------------------------------------------------------
    # Status Updates
    # ----------------------------------------------------------------------
    def mark_done(self, title: str) -> bool:
        """Mark a task as completed"""
        return self.db.update_task_completion(title, True)

    def mark_undone(self, title: str) -> bool:
        """Mark a task as not completed"""
        return self.db.update_task_completion(title, False)

    def toggle_task_status(self, title: str) -> bool:
        """Toggle completion status of a task"""
        task = self.find_task(title)
        if not task:
            return False
        
        # Toggle and update
        new_status = not task.completed
        return self.db.update_task_completion(title, new_status)

    # ----------------------------------------------------------------------
    # Priority Management
    # ----------------------------------------------------------------------
    def update_priority(self, title: str, priority: str) -> bool:
        """Update task priority (low/medium/high)"""
        valid_priorities = {"low", "medium", "high"}
        if priority.lower() not in valid_priorities:
            return False
        return self.db.update_task_priority(title, priority.lower())

    def get_high_priority_tasks(self) -> List[Task]:
        """Return all high priority tasks"""
        all_tasks = self.db.list_tasks()
        return [t for t in all_tasks if t.priority == "high" and not t.completed]

    # ----------------------------------------------------------------------
    # Due Date Management
    # ----------------------------------------------------------------------
    def update_due_date(self, title: str, due_date: Optional[date]) -> bool:
        """Update task due date"""
        return self.db.update_task_due_date(title, due_date)

    def get_overdue_tasks(self) -> List[Task]:
        """Return all overdue (not completed and past due date) tasks"""
        return self.db.list_tasks(filter_by="overdue")

    def get_tasks_due_soon(self, days: int = 3) -> List[Task]:
        """Return tasks due within next 'days' days"""
        today = date.today()
        soon_tasks = []
        
        for task in self.db.list_tasks():
            if not task.completed and task.due_date:
                days_left = (task.due_date - today).days
                if 0 <= days_left <= days:
                    soon_tasks.append(task)
        
        return sorted(soon_tasks, key=lambda x: x.due_date)

    # ----------------------------------------------------------------------
    # Listing with Advanced Filtering
    # ----------------------------------------------------------------------
    def list_tasks(self, filter_by: str = "all") -> None:
        """
        Display tasks with optional filtering.
        filter_by: 'all', 'completed', 'pending', 'overdue', 'high_priority'
        """
        if filter_by == "high_priority":
            tasks = self.get_high_priority_tasks()
        elif filter_by == "overdue":
            tasks = self.get_overdue_tasks()
        elif filter_by in ["completed", "pending"]:
            tasks = self.db.list_tasks(filter_by=filter_by)
        else:
            tasks = self.db.list_tasks()
        
        # Empty list check
        if not tasks:
            self._print_empty_message(filter_by)
            return
        
        # Sort and display
        sorted_tasks = self._sort_tasks(tasks)
        self._display_tasks(sorted_tasks)
        self._print_statistics()

    def _sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by priority and due date.
        Priority order: high > medium > low
        """
        def sort_key(task):
            # Priority weight (high=0, medium=1, low=2)
            priority_weight = {"high": 0, "medium": 1, "low": 2}
            # Overdue penalty: push overdue tasks to top
            overdue_penalty = -1 if (not task.completed and task.is_overdue()) else 0
            # Due date: None = far future
            #date.max=9999-12-31
            due_sort = task.due_date if task.due_date else date.max
            
            return (priority_weight.get(task.priority, 1), overdue_penalty, due_sort)
        
        return sorted(tasks, key=sort_key)

    def _display_tasks(self, tasks: List[Task]) -> None:
        """Print tasks in a formatted list with numbering"""
        print("\n" + "=" * 50)
        
        for i, task in enumerate(tasks, start=1):
            # Use colored output for terminal
            print(f"{i}. {task.format_line(use_color=True)}")
            print("-" * 50)

    def _print_empty_message(self, filter_by: str) -> None:
        """Show appropriate message when no tasks found"""
        messages = {
            "all": "📭 Task list is empty.",
            "completed": "✅ No completed tasks found.",
            "pending": "📌 No pending tasks found.",
            "overdue": "🎉 No overdue tasks! Good job!",
            "high_priority": "🔴 No high priority tasks."
        }
        print(f"\n{messages.get(filter_by, 'No tasks found.')}")

    def _print_statistics(self) -> None:
        """Display task statistics summary"""
        total = self.db.get_task_count()
        completed = self.db.get_task_count(completed=True)
        pending = self.db.get_task_count(completed=False)
        overdue = len(self.get_overdue_tasks())
        
        print(f"\n📊 Statistics:")
        print(f"   Total: {total} | ✅ Done: {completed} | 📌 Pending: {pending} | ⚠️ Overdue: {overdue}")

    # ----------------------------------------------------------------------
    # Search and Filter
    # ----------------------------------------------------------------------
    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description"""
        keyword_lower = keyword.lower()
        all_tasks = self.db.list_tasks()
        
        results = []
        for task in all_tasks:
            if (keyword_lower in task.title.lower() or 
                keyword_lower in task.description.lower()):
                results.append(task)
        
        return results

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Return all tasks with given priority (low/medium/high)"""
        all_tasks = self.db.list_tasks()
        return [t for t in all_tasks if t.priority == priority]

    # ----------------------------------------------------------------------
    # Bulk Operations
    # ----------------------------------------------------------------------
    def mark_all_done(self) -> int:
        """Mark all pending tasks as completed. Returns count of updated tasks."""
        pending_tasks = self.db.list_tasks(filter_by="pending")
        count = 0
        
        for task in pending_tasks:
            if self.mark_done(task.title):
                count += 1
        
        return count

    def delete_all_completed(self) -> int:
        """Delete all completed tasks. Returns number of deleted tasks."""
        completed_tasks = self.db.list_tasks(filter_by="completed")
        count = 0
        
        for task in completed_tasks:
            if self.remove_task(task.title):
                count += 1
        
        return count

    def delete_all_tasks(self) -> int:
        """Delete ALL tasks (caution: irreversible). Returns number of deleted tasks."""
        return self.db.delete_all_tasks()

    # ----------------------------------------------------------------------
    # Cleanup
    # ----------------------------------------------------------------------
    def close(self) -> None:
        """Close database connection"""
        self.db.close()
