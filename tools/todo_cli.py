# tools/todo_cli.py

"""
Simple CLI To-Do List
Beginner-friendly and uses only Python standard library.
Tasks can be marked as done using [x] prefix.
"""

TODO_FILE = "todos.txt"
DONE_PREFIX = "[x] "
TODO_PREFIX = "[ ] "


def load_todos():
    try:
        with open(TODO_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        for todo in todos:
            f.write(todo + "\n")


def is_task_done(task):
    """Check if a task is marked as done."""
    return task.startswith(DONE_PREFIX)


def get_task_text(task):
    """Get the task text without the status prefix."""
    if task.startswith(DONE_PREFIX):
        return task[len(DONE_PREFIX):]
    elif task.startswith(TODO_PREFIX):
        return task[len(TODO_PREFIX):]
    return task


def format_task(task_text, done=False):
    """Format a task with the appropriate status prefix."""
    prefix = DONE_PREFIX if done else TODO_PREFIX
    return prefix + task_text


def show_todos(todos):
    if not todos:
        print("No tasks yet ✨")
        return

    print("\nYour To-Do List:")
    for i, task in enumerate(todos, start=1):
        if is_task_done(task):
            print(f"{i}. {task} ✅")
        else:
            print(f"{i}. {task}")


def mark_task_done(todos, index):
    """Mark a task at the given index as done."""
    if 0 <= index < len(todos):
        task = todos[index]
        if is_task_done(task):
            return False, "Task is already marked as done."
        task_text = get_task_text(task)
        todos[index] = format_task(task_text, done=True)
        return True, f"Marked as done: {task_text}"
    return False, "Invalid task number."


def mark_task_undone(todos, index):
    """Mark a task at the given index as not done."""
    if 0 <= index < len(todos):
        task = todos[index]
        if not is_task_done(task):
            return False, "Task is not marked as done."
        task_text = get_task_text(task)
        todos[index] = format_task(task_text, done=False)
        return True, f"Marked as not done: {task_text}"
    return False, "Invalid task number."


def main():
    todos = load_todos()

    while True:
        print("\n--- To-Do Menu ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Delete task")
        print("4. Mark task as done")
        print("5. Mark task as not done")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            show_todos(todos)

        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                todos.append(format_task(task, done=False))
                save_todos(todos)
                print("Task added ✅")
            else:
                print("Task cannot be empty ❌")

        elif choice == "3":
            show_todos(todos)
            if not todos:
                continue
            try:
                index = int(input("Enter task number to delete: ")) - 1
                if 0 <= index < len(todos):
                    removed = todos.pop(index)
                    save_todos(todos)
                    print(f"Removed: {get_task_text(removed)}")
                else:
                    print("Invalid number ❌")
            except ValueError:
                print("Please enter a number ❌")

        elif choice == "4":
            show_todos(todos)
            if not todos:
                continue
            try:
                index = int(input("Enter task number to mark as done: ")) - 1
                success, message = mark_task_done(todos, index)
                if success:
                    save_todos(todos)
                    print(message + " ✅")
                else:
                    print(message + " ❌")
            except ValueError:
                print("Please enter a number ❌")

        elif choice == "5":
            show_todos(todos)
            if not todos:
                continue
            try:
                index = int(input("Enter task number to mark as not done: ")) - 1
                success, message = mark_task_undone(todos, index)
                if success:
                    save_todos(todos)
                    print(message + " ✅")
                else:
                    print(message + " ❌")
            except ValueError:
                print("Please enter a number ❌")

        elif choice == "6":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option ❌")


if __name__ == "__main__":
    main()
