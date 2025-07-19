import sqlite3
from task import Task

class Database:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            description TEXT,
            due_date TEXT,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, task: Task):
        query = """
        INSERT INTO tasks (title, description, due_date, completed)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.conn.execute(query, (task.title, task.description, task.due_date, int(task.completed)))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_task(self, title: str):
        query = "DELETE FROM tasks WHERE title = ?"
        cursor = self.conn.execute(query, (title,))
        self.conn.commit()
        return cursor.rowcount > 0

    def find_task(self, title: str):
        query = "SELECT * FROM tasks WHERE title = ?"
        cursor = self.conn.execute(query, (title,))
        row = cursor.fetchone()
        if row:
            return self.row_to_task(row)
        return None

    def update_task_completion(self, title: str, completed: bool):
        query = "UPDATE tasks SET completed = ? WHERE title = ?"
        cursor = self.conn.execute(query, (int(completed), title))
        self.conn.commit()
        return cursor.rowcount > 0

    def list_tasks(self):
        query = "SELECT * FROM tasks"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        return [self.row_to_task(row) for row in rows]

    def row_to_task(self, row):
        task = Task(
            title=row["title"],
            description=row["description"],
            due_date=row["due_date"]
        )
        task.completed = bool(row["completed"])
        return task

    def close(self):
        self.conn.close()
