# tools/todo_cli.py

"""
Simple CLI To-Do List
Beginner-friendly and uses only Python standard library.
Now with MARK COMPLETE feature! ✅
"""

TODO_FILE = "todos.txt"


def load_todos():
    """Load todos from file, preserving [x] status markers."""
    try:
        with open(TODO_FILE, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []


def save_todos(todos):
    """Save todos to file."""
    with open(TODO_FILE, "w") as f:
        for todo in todos:
            f.write(todo + "\n")


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
                todos.append(task)
                save_todos(todos)
                print("✅ Task added!")
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
