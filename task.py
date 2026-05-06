# task.py
"""
Task model for Todo Manager
Supports priority, due date, overdue check, and timestamps
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single task with title, description, due date, priority, and completion status.
    Automatically tracks creation and update timestamps.
    """

    title: str                       # Required
    description: str = ""            # Optional 
    due_date: Optional[date] = None  #  date object (YYYY-MM-DD)
    completed: bool = False          
    priority: str = "medium"          #  'low', 'medium', 'high'

    # Auto timestamps 
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate priority and ensure due_date is date or None."""
        valid_priorities = {"low", "medium", "high"}
        if self.priority not in valid_priorities:
            self.priority = "medium"          # fallback to default

        # If due_date was provided as string (e.g., from JSON), convert it
        if isinstance(self.due_date, str):
            self.due_date = self._parse_date(self.due_date)

    # ----------------------------------------------------------------------
    # Status changers
    # ----------------------------------------------------------------------
    def mark_done(self) -> None:
        self.completed = True
        self.updated_at = datetime.now()

    def mark_undone(self) -> None:
        self.completed = False
        self.updated_at = datetime.now()

    def toggle(self) -> None:
        """Flip completion status and update timestamp."""
        self.completed = not self.completed
        self.updated_at = datetime.now()

    # ----------------------------------------------------------------------
    # Overdue check
    # ----------------------------------------------------------------------
    def is_overdue(self, reference_date: Optional[date] = None) -> bool:
        """
        Return True if task is not completed and due_date is before today.
        If reference_date is given, use it instead of today.
        """
        if self.completed or self.due_date is None:
            return False
        if reference_date is None:
            reference_date = date.today()
        return self.due_date < reference_date

    # ----------------------------------------------------------------------
    # Serialization helpers (to/from dict, string date handling)
    # ----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON storage."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create a Task instance from dictionary (e.g., loaded from JSON)."""
        # Parse date strings back to date objects
        due = data.get("due_date")
        if due and isinstance(due, str):
            due = Task._parse_date(due)

        # Parse datetime strings if present, fallback to now
        created = data.get("created_at")
        if created and isinstance(created, str):
            created = datetime.fromisoformat(created)
        else:
            created = datetime.now()

        updated = data.get("updated_at")
        if updated and isinstance(updated, str):
            updated = datetime.fromisoformat(updated)
        else:
            updated = created

        return Task(
            title=data["title"],
            description=data.get("description", ""),
            due_date=due,
            completed=data.get("completed", False),
            priority=data.get("priority", "medium"),
            created_at=created,
            updated_at=updated,
        )

    @staticmethod
    def _parse_date(date_str: str) -> Optional[date]:
        """Parse a date string in YYYY-MM-DD format; return None if invalid."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None

    # ----------------------------------------------------------------------
    # Display 
    # ----------------------------------------------------------------------
   
    def format_line(self, use_color: bool = True) -> str:
        """
        Return a human-readable line for terminal output.
        Includes status icon, priority marker, and overdue warning.
        """
        if use_color:
            from colorama import Fore, Style

        # Status icon and color
        if self.completed:
            status_icon = "✅"
            status_text = "انجام شده" if use_color else "[Done]"
            color = Fore.GREEN if use_color else ""
        else:
            status_icon = "📌"
            status_text = "انجام نشده" if use_color else "[Pending]"
            color = Fore.YELLOW if use_color else ""

        # Priority icon
        priority_icon = {"low": "🟢", "medium": "🟠", "high": "🔴"}.get(self.priority, "⚪")

        result = f"{color}{status_icon} {self.title} - {status_text} [{priority_icon}]"

        # Overdue warning (only if not completed and overdue)
        if not self.completed and self.is_overdue():
            warning = " ⚠️ OVERDUE!" if not use_color else f" {Fore.RED}⚠️ ددلاین گذشته{Style.RESET_ALL}"
            result += warning

        if use_color:
            result += Style.RESET_ALL

        # Add description and due date if present
        if self.description:
            result += f"\n   📝 {self.description}"
        if self.due_date:
            result += f"\n   📅 Due: {self.due_date.isoformat()}"

        return result

    def __str__(self) -> str:
        """
        Simple string representation (without color) for debugging.
        Use format_line() for rich terminal output.
        """
        return f"Task({self.title!r}, completed={self.completed}, priority={self.priority}, due={self.due_date})"

    def __repr__(self) -> str:
        return self.__str__()
