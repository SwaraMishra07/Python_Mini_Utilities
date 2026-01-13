"""
Simple CLI To-Do List
Beginner-friendly and uses only Python standard library.

Improvements:
- atomic file writes to avoid lost writes when multiple processes write
- helper `add_task()` to prevent duplicates
Now with MARK COMPLETE feature! ✅
"""

import os
import tempfile

TODO_FILE = "todos.txt"
MAX_TASK_LEN = 36


def _todo_path():
    return os.path.join(os.path.dirname(__file__), TODO_FILE)


def load_todos():
    """Load todos from file, preserving [x] status markers."""
    path = _todo_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
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


def is_completed(task):
    """Check if task is marked as completed."""
    return task.startswith("[x] ") or task.startswith("[x]")


def toggle_completion(task):
    """Toggle [ ] / [x] status of a task."""
    if is_completed(task):
        # Remove [x] marker → return plain task
        return task[4:] if task.startswith("[x] ") else task[3:]
    else:
        # Add [x] marker → return marked task
        return f"[x] {task}"


def show_todos(todos):
    """Display todos with completion status."""
    if not todos:
        print("No tasks yet ✨")
        return

    print("\n📋 Your To-Do List:")
    completed_count = 0
    
    for i, task in enumerate(todos, start=1):
        status = "✅" if is_completed(task) else "⏳"
        display_task = task[4:] if task.startswith("[x] ") else task
        print(f"{i:2d}. [{status}] {display_task}")
        if is_completed(task):
            completed_count += 1
    
    print(f"\n({len(todos) - completed_count} pending, {completed_count} done)")


def main():
    todos = load_todos()

    while True:
        print("\n" + "="*25)
        print("🎯 TO-DO MENU")
        print("1. View tasks")
        print("2. Add task") 
        print("3. Delete task")
        print("4. Mark Done")  
        print("5. Exit")
        print("="*25)

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            show_todos(todos)

        elif choice == "2":
            task = input("➕ New task: ").strip()
            if task:
                added = add_task(task)
                if added:
                    todos = load_todos()
                    print("Task added ✅")
                else:
                    print("Task is a duplicate or empty ❌")
            else:
                print("❌ Task cannot be empty")

        elif choice == "3":
            show_todos(todos)
            if todos:
                try:
                    index = int(input("🗑️  Task number to delete: ")) - 1
                    if 0 <= index < len(todos):
                        removed = todos.pop(index)
                        save_todos(todos)
                        print(f"🗑️  Removed: {removed}")
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Enter a valid number")

        elif choice == "4":  # ← NEW MARK FEATURE
            show_todos(todos)
            if todos:
                try:
                    index = int(input("✅ Task number to toggle: ")) - 1
                    if 0 <= index < len(todos):
                        old_task = todos[index]
                        todos[index] = toggle_completion(old_task)
                        save_todos(todos)
                        new_status = "marked DONE ✅" if is_completed(todos[index]) else "marked PENDING ⏳"
                        print(f"Toggle: {old_task} → {new_status}")
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Enter a valid number")
            else:
                print("No tasks to mark!")

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option (1-5)")


if __name__ == "__main__":
    main()
