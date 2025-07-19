from colorama import Fore, init
init(autoreset=True)

import json
import os
from task import Task
from manager import TaskManager


# ---------- Load Language ----------
def load_language(lang_code):
    file_path = f"{lang_code}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print(f"⚠️ Language file '{file_path}' not found. Falling back to English.")
        with open("en.json", "r", encoding="utf-8") as f:
            return json.load(f)


# ---------- Main Program ----------
def main():
    # Ask language
    lang = input("Choose language / زبان را انتخاب کنید (en/fa): ").strip().lower()
    print(f"Input lang: '{lang}'")

    if lang == "fa":
        print("فارسی انتخاب شد")
    elif lang == "en":
        print("English selected")
    else:
        print("Language not supported, defaulting to English")
        lang = "en"

    msg = load_language(lang)

    manager = TaskManager()

    while True:
        print(Fore.BLUE + "\n" + msg["menu_title"])
        for line in msg["menu_options"]:
            print(line)

        choice = input(msg["prompt_choice"]).strip()

        if choice == "1":
            manager.list_tasks()

        elif choice == "2":
            title = input(msg["add_title"]).strip()
            description = input(msg["add_description"]).strip()
            due_date = input(msg["add_due_date"]).strip()
            due_date = due_date if due_date else None

            if manager.find_task(title):
                print(Fore.RED + msg["task_exists"])
            else:
                task = Task(title, description, due_date)
                manager.add_task(task)
                print(Fore.CYAN + msg["task_added"].format(title=title))

        elif choice == "3":
            title = input(msg["input_delete"]).strip()
            if manager.remove_task(title):
                print(Fore.CYAN + msg["task_deleted"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))

        elif choice == "4":
            title = input(msg["input_done"]).strip()
            if manager.mark_done(title):
                print(Fore.CYAN + msg["mark_done"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))

        elif choice == "5":
            title = input(msg["input_undone"]).strip()
            if manager.mark_undone(title):
                print(Fore.CYAN + msg["mark_undone"].format(title=title))
            else:
                print(Fore.RED + msg["task_not_found"].format(title=title))

        elif choice == "6":
            print(Fore.GREEN + msg["exit_msg"])
            manager.close()
            break

        else:
            print(Fore.RED + msg["invalid_choice"])


if __name__ == "__main__":
    main()
