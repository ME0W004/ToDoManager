# main.py
"""
Main entry point for Task Manager CLI application
Supports dual language (English/Persian) with colorful terminal output
"""

from colorama import Fore, init
init(autoreset=True)  # Auto-reset colors after each print

import json
import os
from datetime import date, datetime
from task import Task
from manager import TaskManager


# ----------------------------------------------------------------------
# Language Loading
# ----------------------------------------------------------------------
def load_language(lang_code: str) -> dict:
    """Load language JSON file. Fallback to English if not found."""
    file_path = f"{lang_code}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print(f"⚠️ Language file '{file_path}' not found. Falling back to English.")
        with open("en.json", "r", encoding="utf-8") as f:
            return json.load(f)


# ----------------------------------------------------------------------
# Input Helpers
# ----------------------------------------------------------------------
def get_priority_input(msg: dict, lang: str) -> str:
    """Get and validate priority input from user."""
    priority = input(msg["add_priority"]).strip().lower()
    if priority not in ["low", "medium", "high"]:
        print(Fore.YELLOW + f"⚠️ Invalid priority. Using default: medium")
        return "medium"
    return priority


def get_due_date_input(prompt: str) -> date:
    """Parse due date string to date object. Return None if invalid/empty."""
    due_str = input(prompt).strip()
    if not due_str:
        return None
    
    try:
        return datetime.strptime(due_str, "%Y-%m-%d").date()
    except ValueError:
        print(Fore.YELLOW + "⚠️ Invalid date format. Use YYYY-MM-DD. Skipping...")
        return None


def confirm_action(msg: str) -> bool:
    """Ask for user confirmation (yes/no)."""
    response = input(msg).strip().lower()
    return response == "yes" or response == "y"


# ----------------------------------------------------------------------
# Display Helpers
# ----------------------------------------------------------------------
def display_search_results(results, keyword: str, msg: dict) -> None:
    """Display search results in formatted way."""
    if not results:
        print(Fore.YELLOW + msg["search_no_results"].format(keyword=keyword))
        return
    
    print(Fore.CYAN + "\n" + msg["search_results"].format(keyword=keyword))
    print("=" * 50)
    for i, task in enumerate(results, start=1):
        print(f"{i}. {task.format_line(use_color=True)}")
        print("-" * 50)


# ----------------------------------------------------------------------
# Main Program
# ----------------------------------------------------------------------
def main():
    """Main application entry point with menu loop."""
    
    # Language selection
    print(Fore.CYAN + "=== Task Manager ===")
    lang = input("Choose language / زبان را انتخاب کنید (en/fa): ").strip().lower()
    
    if lang == "fa":
        print(Fore.GREEN + "فارسی انتخاب شد")
    elif lang == "en":
        print(Fore.GREEN + "English selected")
    else:
        print(Fore.YELLOW + "Language not supported, defaulting to English")
        lang = "en"
    
    # Load language file
    msg = load_language(lang)
    manager = TaskManager()
    
    # Main menu loop
    while True:
        print(Fore.BLUE + "\n" + msg["menu_title"])
        for line in msg["menu_options"]:
            print(line)
        
        choice = input(msg["prompt_choice"]).strip()
        
        # ------------------------------------------------------------------
        # Display Options (1-5)
        # ------------------------------------------------------------------
        if choice == "1":
            manager.list_tasks(filter_by="all")
        
        elif choice == "2":
            manager.list_tasks(filter_by="completed")
        
        elif choice == "3":
            manager.list_tasks(filter_by="pending")
        
        elif choice == "4":
            manager.list_tasks(filter_by="overdue")
        
        elif choice == "5":
            manager.list_tasks(filter_by="high_priority")
        
        # ------------------------------------------------------------------
        # Add Task (6)
        # ------------------------------------------------------------------
        elif choice == "6":
            title = input(msg["add_title"]).strip()
            if not title:
                print(Fore.RED + "⚠️ Title cannot be empty!")
                continue
            
            if manager.find_task(title):
                print(Fore.RED + msg["task_exists"])
                continue
            
            description = input(msg["add_description"]).strip()
            due_date = get_due_date_input(msg["add_due_date"])
            priority = get_priority_input(msg, lang)
            
            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority
            )
            
            if manager.add_task(task):
                print(Fore.GREEN + msg["task_added"].format(title=title))
            else:
                print(Fore.RED + "❌ Failed to add task!")
        
        # ------------------------------------------------------------------
        # Delete Task (7)
        # ------------------------------------------------------------------
        elif choice == "7":
            title = input(msg["input_delete"]).strip()
            if manager.remove_task(title):
                print(Fore.GREEN + msg["task_deleted"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))
        
        # ------------------------------------------------------------------
        # Search Tasks (8)
        # ------------------------------------------------------------------
        elif choice == "8":
            keyword = input(msg["input_search"]).strip()
            if keyword:
                results = manager.search_tasks(keyword)
                display_search_results(results, keyword, msg)
            else:
                print(Fore.YELLOW + "⚠️ Please enter a search keyword.")
        
        # ------------------------------------------------------------------
        # Status Updates (9-11)
        # ------------------------------------------------------------------
        elif choice == "9":
            title = input(msg["input_done"]).strip()
            if manager.mark_done(title):
                print(Fore.GREEN + msg["mark_done"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))
        
        elif choice == "10":
            title = input(msg["input_undone"]).strip()
            if manager.mark_undone(title):
                print(Fore.GREEN + msg["mark_undone"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))
        
        elif choice == "11":
            title = input(msg["input_toggle"]).strip()
            if manager.toggle_task_status(title):
                print(Fore.GREEN + msg["task_toggled"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))
        
        # ------------------------------------------------------------------
        # Update Operations (12-13)
        # ------------------------------------------------------------------
        elif choice == "12":
            title = input("Enter task title: ").strip()
            task = manager.find_task(title)
            if not task:
                print(Fore.RED + msg["task_not_found"].format(title=title))
                continue
            
            new_priority = get_priority_input(msg, lang)
            if manager.update_priority(title, new_priority):
                print(Fore.GREEN + msg["priority_updated"].format(
                    title=title, priority=new_priority
                ))
        
        elif choice == "13":
            title = input("Enter task title: ").strip()
            task = manager.find_task(title)
            if not task:
                print(Fore.RED + msg["task_not_found"].format(title=title))
                continue
            
            new_due_date = get_due_date_input(msg["input_due_date_new"])
            if manager.update_due_date(title, new_due_date):
                if new_due_date:
                    print(Fore.GREEN + msg["due_date_updated"].format(
                        title=title, due_date=new_due_date.isoformat()
                    ))
                else:
                    print(Fore.GREEN + msg["due_date_removed"].format(title=title))
        
        # ------------------------------------------------------------------
        # Bulk Operations (14-16)
        # ------------------------------------------------------------------
        elif choice == "14":
            count = manager.mark_all_done()
            print(Fore.GREEN + msg["all_tasks_done"].format(count=count))
        
        elif choice == "15":
            count = manager.delete_all_completed()
            print(Fore.GREEN + msg["all_completed_deleted"].format(count=count))
        
        elif choice == "16":
            print(Fore.RED + "⚠️  WARNING! This will delete ALL tasks!  ⚠️")
            if confirm_action(msg["confirm_delete_all"]):
                count = manager.delete_all_tasks()
                print(Fore.RED + msg["all_tasks_deleted"].format(count=count))
            else:
                print(Fore.YELLOW + "Operation cancelled.")
        
        # ------------------------------------------------------------------
        # Statistics (17)
        # ------------------------------------------------------------------
        elif choice == "17":
            # Use manager's internal method to show stats
            manager.list_tasks(filter_by="all")  # This shows stats too
        
        # ------------------------------------------------------------------
        # Exit (18)
        # ------------------------------------------------------------------
        elif choice == "18":
            print(Fore.GREEN + msg["exit_msg"])
            manager.close()
            break
        
        # ------------------------------------------------------------------
        # Invalid Input
        # ------------------------------------------------------------------
        else:
            print(Fore.RED + msg["invalid_choice"])


# ----------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
