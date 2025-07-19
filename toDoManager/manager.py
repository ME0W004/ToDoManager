from task import Task
from data.db import Database

class TaskManager:
    def __init__(self):
        self.db = Database()

    def add_task(self, task: Task) -> bool:
        return self.db.add_task(task)

    def remove_task(self, title: str) -> bool:
        return self.db.remove_task(title)

    def mark_done(self, title: str) -> bool:
        return self.db.update_task_completion(title, True)

    def mark_undone(self, title: str) -> bool:
        return self.db.update_task_completion(title, False)

    def list_tasks(self):
        tasks = self.db.list_tasks()
        if not tasks:
            print("📭 لیست وظایف خالی است.")
            return

        from datetime import datetime
        with_due = []
        without_due = []

        for task in tasks:
            if task.due_date:
                try:
                    due = datetime.strptime(task.due_date, "%Y-%m-%d")
                    with_due.append((due, task))
                except ValueError:
                    without_due.append(task)
            else:
                without_due.append(task)

        with_due.sort(key=lambda x: x[0])
        sorted_tasks = [t for _, t in with_due] + without_due

        for i, task in enumerate(sorted_tasks, start=1):
            print(f"{i}. {task}")

        print(f"\n📦 مجموع تسک‌ها: {len(tasks)}")

    def find_task(self, title: str):
        return self.db.find_task(title)

    def close(self):
        self.db.close()
