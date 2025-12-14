"""
Tests for todo_cli.py mark as done functionality.
"""

import sys
import os

# Add tools directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from todo_cli import (
    is_task_done,
    get_task_text,
    format_task,
    mark_task_done,
    mark_task_undone,
    DONE_PREFIX,
    TODO_PREFIX,
)


class TestIsTaskDone:
    """Tests for is_task_done function."""

    def test_done_task(self):
        """Test that task with [x] prefix is detected as done."""
        assert is_task_done("[x] Buy groceries") is True

    def test_undone_task(self):
        """Test that task with [ ] prefix is detected as not done."""
        assert is_task_done("[ ] Buy groceries") is False

    def test_task_without_prefix(self):
        """Test that task without prefix is detected as not done."""
        assert is_task_done("Buy groceries") is False


class TestGetTaskText:
    """Tests for get_task_text function."""

    def test_done_task_text(self):
        """Test extracting text from done task."""
        assert get_task_text("[x] Buy groceries") == "Buy groceries"

    def test_undone_task_text(self):
        """Test extracting text from undone task."""
        assert get_task_text("[ ] Buy groceries") == "Buy groceries"

    def test_task_without_prefix(self):
        """Test extracting text from task without prefix."""
        assert get_task_text("Buy groceries") == "Buy groceries"


class TestFormatTask:
    """Tests for format_task function."""

    def test_format_done_task(self):
        """Test formatting task as done."""
        assert format_task("Buy groceries", done=True) == "[x] Buy groceries"

    def test_format_undone_task(self):
        """Test formatting task as not done."""
        assert format_task("Buy groceries", done=False) == "[ ] Buy groceries"

    def test_format_default_is_undone(self):
        """Test that default formatting is undone."""
        assert format_task("Buy groceries") == "[ ] Buy groceries"


class TestMarkTaskDone:
    """Tests for mark_task_done function."""

    def test_mark_undone_task_as_done(self):
        """Test marking an undone task as done."""
        todos = ["[ ] Buy groceries", "[ ] Clean room"]
        success, message = mark_task_done(todos, 0)
        assert success is True
        assert "Marked as done" in message
        assert todos[0] == "[x] Buy groceries"

    def test_mark_already_done_task(self):
        """Test marking an already done task."""
        todos = ["[x] Buy groceries"]
        success, message = mark_task_done(todos, 0)
        assert success is False
        assert "already marked as done" in message.lower()

    def test_mark_invalid_index(self):
        """Test marking with invalid index."""
        todos = ["[ ] Buy groceries"]
        success, message = mark_task_done(todos, 10)
        assert success is False
        assert "Invalid" in message

    def test_mark_negative_index(self):
        """Test marking with negative index."""
        todos = ["[ ] Buy groceries"]
        success, message = mark_task_done(todos, -1)
        assert success is False
        assert "Invalid" in message


class TestMarkTaskUndone:
    """Tests for mark_task_undone function."""

    def test_mark_done_task_as_undone(self):
        """Test marking a done task as undone."""
        todos = ["[x] Buy groceries", "[ ] Clean room"]
        success, message = mark_task_undone(todos, 0)
        assert success is True
        assert "Marked as not done" in message
        assert todos[0] == "[ ] Buy groceries"

    def test_mark_already_undone_task(self):
        """Test marking an already undone task."""
        todos = ["[ ] Buy groceries"]
        success, message = mark_task_undone(todos, 0)
        assert success is False
        assert "not marked as done" in message.lower()

    def test_mark_undone_invalid_index(self):
        """Test marking undone with invalid index."""
        todos = ["[x] Buy groceries"]
        success, message = mark_task_undone(todos, 10)
        assert success is False
        assert "Invalid" in message


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
