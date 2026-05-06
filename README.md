# 📝 ToDoManager

A simple and powerful command-line To-Do List application built with Python and SQLite.  
Supports **multi-language (English & Persian)** and features a **colored terminal UI** using the `colorama` library.

---

## 🚀 Features

- ➕ Add, remove, and manage tasks
- ✅ Mark tasks as done/undone
- 🔄 Toggle task status (done/undone)
- 📅 Set due dates with overdue detection
- 🎯 Priority levels (High, Medium, Low)
- 🔍 Search tasks by title or description
- 📊 View statistics (total, completed, pending, overdue)
- 🗄️ Persistent storage using SQLite database
- 🌍 Multilingual support (English and Persian)
- 🎨 Colored CLI output using `colorama`
- 📋 Smart sorting by priority and due date
- ⚡ Bulk operations (mark all done, delete completed)

---

## Usage Examples

 English Session Example
text
=== Task Manager ===
Choose language / زبان را انتخاب کنید (en/fa): en
English selected

=== Task Manager Menu ===
1. Show all tasks
2. Show completed tasks
3. Show pending tasks
4. Show overdue tasks
5. Show high priority tasks
6. Add new task
7. Delete task
8. Search tasks
9. Mark task as done
10. Mark task as not done
11. Toggle task status
12. Update task priority
13. Update task due date
14. Mark all tasks as done
15. Delete all completed tasks
16. Delete ALL tasks (warning!)
17. Show task statistics
18. Exit

Enter your choice (1-18): 6
Task title: Complete Python project
Description (optional): Finish ToDoManager app
Due date (e.g., 2025-07-10) (optional): 2025-06-15
Priority (low/medium/high) (default: medium): high
✅ Task 'Complete Python project' added.

Enter your choice (1-18): 1

==================================================
1. 📌 Complete Python Project - Pending [🔴]
   📝 Finish ToDoManager app
   📅 Due: 2025-06-15
--------------------------------------------------

📊 Statistics:
   Total: 1 | ✅ Done: 0 | 📌 Pending: 1 | ⚠️ Overdue: 0

Enter your choice (1-18): 9
Enter title of task to mark as done: Complete Python project
✅ Task 'Complete Python project' marked as done.

Enter your choice (1-18): 1

==================================================
1. ✅ Complete Python Project - Done [🔴]
   📝 Finish ToDoManager app
   📅 Due: 2025-06-15
--------------------------------------------------

📊 Statistics:
   Total: 1 | ✅ Done: 1 | 📌 Pending: 0 | ⚠️ Overdue: 0

Enter your choice (1-18): 18
Exiting program. Goodbye! 👋


## 📦 Requirements

- Python 3.8 or higher  
- Dependencies:
  - `colorama`

### Install requirements:

```bash
pip install colorama
