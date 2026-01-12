from flask import Flask, render_template_string, request, redirect, url_for

from todo_cli import load_todos, save_todos


app = Flask(__name__)


TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>To-Do List</title>
    <style>
      body {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
          sans-serif;
        margin: 0;
        padding: 0;
        background: #f3f4f6;
        color: #111827;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
      }
      .container {
        background: #ffffff;
        padding: 24px 28px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
        width: 100%;
        max-width: 480px;
      }
      h1 {
        margin: 0 0 16px;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      h1 span {
        font-size: 1.25rem;
      }
      form.add-form {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
      }
      input[type="text"] {
        flex: 1;
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-size: 0.95rem;
      }
      input[type="text"]:focus {
        outline: none;
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.35);
      }
      button {
        border: none;
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }
      button.primary {
        background: #2563eb;
        color: white;
      }
      button.primary:hover {
        background: #1d4ed8;
      }
      ul {
        list-style: none;
        padding: 0;
        margin: 0;
      }
      li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #e5e7eb;
      }
      li:last-child {
        border-bottom: none;
      }
      .empty {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        padding: 10px 0 2px;
      }
      .delete-btn {
        background: transparent;
        color: #ef4444;
        padding: 4px 6px;
      }
      .delete-btn:hover {
        color: #b91c1c;
      }
      small {
        display: block;
        margin-top: 10px;
        color: #9ca3af;
        font-size: 0.75rem;
        text-align: right;
      }
      @media (max-width: 600px) {
        .container {
          margin: 16px;
          padding: 20px;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>
        To-Do List
        <span>✅</span>
      </h1>

      <form class="add-form" method="post" action="{{ url_for('add_todo') }}">
        <input
          type="text"
          name="task"
          placeholder="Add a new task..."
          autocomplete="off"
          required
        />
        <button class="primary" type="submit">Add</button>
      </form>

      {% if todos %}
      <ul>
        {% for i, task in enumerate(todos) %}
        <li>
          <span>{{ i + 1 }}. {{ task }}</span>
          <form
            method="post"
            action="{{ url_for('delete_todo', index=i) }}"
            style="margin: 0"
          >
            <button class="delete-btn" type="submit" title="Delete task">
              ✕
            </button>
          </form>
        </li>
        {% endfor %}
      </ul>
      {% else %}
      <div class="empty">No tasks yet ✨</div>
      {% endif %}

      <small>Stored in tools/todos.txt and shared with the CLI.</small>
    </div>
  </body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    todos = load_todos()
    return render_template_string(TEMPLATE, todos=todos, enumerate=enumerate)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task", "").strip()
    if task:
        todos = load_todos()
        todos.append(task)
        save_todos(todos)
    return redirect(url_for("index"))


@app.route("/delete/<int:index>", methods=["POST"])
def delete_todo(index: int):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

