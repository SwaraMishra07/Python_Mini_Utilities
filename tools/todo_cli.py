"""
Simple CLI To-Do List
Beginner-friendly and uses only Python standard library.

Improvements:
- atomic file writes to avoid lost writes when multiple processes write
- helper `add_task()` to prevent duplicates
"""

import os
import tempfile

TODO_FILE = "todos.txt"
MAX_TASK_LEN = 36


def _todo_path():
    return os.path.join(os.path.dirname(__file__), TODO_FILE)


def load_todos():
    path = _todo_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def save_todos(todos):
    """Atomically write todos to disk to avoid lost writes from concurrent writers."""
    path = _todo_path()
    dirpath = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(prefix=TODO_FILE, dir=dirpath)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for todo in todos:
                f.write(todo + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except OSError:
            pass


def add_task(task: str) -> bool:
    """Add `task` if it's not a duplicate (case-insensitive). Returns True if added."""
    task = task.strip()
    if not task:
        return False
    if len(task) > MAX_TASK_LEN:
        task = task[:MAX_TASK_LEN]
    todos = load_todos()
    normalized = {t.strip().lower() for t in todos}
    if task.lower() in normalized:
        return False
    todos.append(task)
    save_todos(todos)
    return True


def show_todos(todos):
    if not todos:
        print("No tasks yet ✨")
        return

    print("\nYour To-Do List:")
    for i, task in enumerate(todos, start=1):
        print(f"{i}. {task}")


def main():
    todos = load_todos()

    while True:
        print("\n--- To-Do Menu ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Delete task")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            show_todos(todos)

        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                added = add_task(task)
                if added:
                    todos = load_todos()
                    print("Task added ✅")
                else:
                    print("Task is a duplicate or empty ❌")
            else:
                print("Task cannot be empty ❌")

        elif choice == "3":
            show_todos(todos)
            try:
                index = int(input("Enter task number to delete: ")) - 1
                if 0 <= index < len(todos):
                    removed = todos.pop(index)
                    save_todos(todos)
                    print(f"Removed: {removed}")
                else:
                    print("Invalid number ❌")
            except ValueError:
                print("Please enter a number ❌")

        elif choice == "4":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option ❌")


if __name__ == "__main__":
    main()
