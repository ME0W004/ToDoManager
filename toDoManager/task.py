from colorama import Fore, Style

class Task:
    def __init__(self, title, description="", due_date=None, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def mark_done(self):
        self.completed = True

    def mark_undone(self):
        self.completed = False

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", None),
            completed=data.get("completed", False)
        )

    def __str__(self):
        status_icon = "✅" if self.completed else "📌"
        status_text = "انجام شده" if self.completed else "انجام نشده"
        color = Fore.GREEN if self.completed else Fore.YELLOW

        result = f"{color}{status_icon} {self.title} - {status_text}{Style.RESET_ALL}"

        if self.description:
            result += f"\n 📝 توضیح: {self.description}"

        if self.due_date:
            result += f"\n 📅 مهلت: {self.due_date}"

        return result
