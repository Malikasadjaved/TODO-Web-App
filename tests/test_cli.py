"""Tests for CLI interface."""

from datetime import datetime

from src.todo.cli import format_task, display_menu
from src.todo.models import Task, Priority


class TestFormatTask:
    """Test format_task function."""

    def test_format_task_output(self):
        """Test that format_task returns formatted string."""
        task = Task(
            id=1,
            title="Test Task",
            description="Description",
            status="incomplete",
            priority=Priority.HIGH,
        )

        output = format_task(task)

        assert "1" in output  # ID
        assert "Test Task" in output  # Title
        assert "HIGH" in output or "[H]" in output  # Priority indicator

    def test_format_task_with_overdue(self):
        """Test format_task shows overdue indicator."""
        task = Task(
            id=1,
            title="Overdue Task",
            due_date=datetime(2020, 1, 1),
            status="incomplete",
        )

        output = format_task(task)

        assert "[!]" in output or "overdue" in output.lower()


class TestDisplayMenu:
    """Test display_menu function."""

    def test_menu_display(self, capsys):
        """Test that display_menu prints the menu."""
        display_menu()

        captured = capsys.readouterr()
        output = captured.out

        # Check for tier labels
        assert "PRIMARY" in output or "Core" in output
        assert "INTERMEDIATE" in output or "Organization" in output
        assert "ADVANCED" in output or "Automation" in output

        # Check for basic options
        assert "Add" in output or "1" in output
        assert "View" in output or "2" in output
        assert "Exit" in output or "0" in output


class TestPriorityDisplay:
    """Test priority display indicators (US2)."""

    def test_priority_display_indicators(self):
        """Test that priority indicators are displayed correctly."""
        # Test HIGH priority
        high_task = Task(id=1, title="High Priority", priority=Priority.HIGH)
        high_output = format_task(high_task)
        assert "[H]" in high_output

        # Test MEDIUM priority
        medium_task = Task(id=2, title="Medium Priority", priority=Priority.MEDIUM)
        medium_output = format_task(medium_task)
        assert "[M]" in medium_output

        # Test LOW priority
        low_task = Task(id=3, title="Low Priority", priority=Priority.LOW)
        low_output = format_task(low_task)
        assert "[L]" in low_output

    def test_tags_display_with_visual_separators(self):
        """Test that tags are displayed with visual separators."""
        task = Task(id=1, title="Tagged Task", tags=["Work", "Urgent", "Meeting"])
        output = format_task(task)

        # Check that tags appear in output
        assert "Work" in output
        assert "Urgent" in output
        assert "Meeting" in output

        # Check for tag separator (# symbol from cli.py)
        assert "#" in output


class TestDueDateDisplay:
    """Test due date and overdue indicators (US3)."""

    def test_overdue_indicator_display(self):
        """Test that overdue indicator [!] is displayed for past due tasks."""
        # Overdue incomplete task
        overdue_task = Task(
            id=1,
            title="Overdue Task",
            due_date=datetime(2020, 1, 1),
            status="incomplete",
        )
        overdue_output = format_task(overdue_task)
        assert "[!]" in overdue_output

        # Future task - no overdue indicator
        future_task = Task(id=2, title="Future Task", due_date=datetime(2099, 12, 31))
        future_output = format_task(future_task)
        assert "[!]" not in future_output

    def test_due_date_formatting(self):
        """Test that due dates are displayed in correct format."""
        task_with_date = Task(
            id=1, title="Task with due date", due_date=datetime(2025, 12, 31, 14, 30)
        )
        output = format_task(task_with_date)

        # Check for date components
        assert "2025-12-31" in output
        assert "14:30" in output
        assert "Due:" in output or "due" in output.lower()

    def test_task_type_display(self):
        """Test that task type is displayed correctly."""
        # Scheduled task
        scheduled = Task(id=1, title="Scheduled", due_date=datetime(2025, 12, 31))
        scheduled_output = format_task(scheduled)
        assert "[scheduled]" in scheduled_output

        # Activity task
        activity = Task(id=2, title="Activity")
        activity_output = format_task(activity)
        assert "[activity]" in activity_output


class TestSelectPriority:
    """Test priority selection menu (F013 - User Story 1)."""

    def test_select_priority_high(self, monkeypatch):
        """Test selecting HIGH priority (option 1)."""
        from src.todo.cli import select_priority

        monkeypatch.setattr("builtins.input", lambda _: "1")
        priority = select_priority()
        assert priority == Priority.HIGH

    def test_select_priority_medium(self, monkeypatch):
        """Test selecting MEDIUM priority (option 2)."""
        from src.todo.cli import select_priority

        monkeypatch.setattr("builtins.input", lambda _: "2")
        priority = select_priority()
        assert priority == Priority.MEDIUM

    def test_select_priority_low(self, monkeypatch):
        """Test selecting LOW priority (option 3)."""
        from src.todo.cli import select_priority

        monkeypatch.setattr("builtins.input", lambda _: "3")
        priority = select_priority()
        assert priority == Priority.LOW

    def test_select_priority_default_empty_input(self, monkeypatch):
        """Test that empty input defaults to MEDIUM."""
        from src.todo.cli import select_priority

        monkeypatch.setattr("builtins.input", lambda _: "")
        priority = select_priority()
        assert priority == Priority.MEDIUM

    def test_select_priority_invalid_input(self, monkeypatch, capsys):
        """Test that invalid input defaults to MEDIUM with error message."""
        from src.todo.cli import select_priority

        monkeypatch.setattr("builtins.input", lambda _: "99")
        priority = select_priority()
        assert priority == Priority.MEDIUM

        captured = capsys.readouterr()
        assert "Invalid" in captured.out or "invalid" in captured.out

    def test_select_priority_invalid_text(self, monkeypatch, capsys):
        """Test that text input defaults to MEDIUM with error message."""
        from src.todo.cli import select_priority

        monkeypatch.setattr("builtins.input", lambda _: "abc")
        priority = select_priority()
        assert priority == Priority.MEDIUM

        captured = capsys.readouterr()
        assert "Invalid" in captured.out or "invalid" in captured.out


class TestSelectRecurrence:
    """Test recurrence selection menu (F013 - User Story 2)."""

    def test_select_recurrence_none(self, monkeypatch):
        """Test selecting no recurrence (option 0)."""
        from src.todo.cli import select_recurrence

        monkeypatch.setattr("builtins.input", lambda _: "0")
        recurrence = select_recurrence()
        assert recurrence is None

    def test_select_recurrence_daily(self, monkeypatch):
        """Test selecting DAILY recurrence (option 1)."""
        from src.todo.cli import select_recurrence
        from src.todo.models import RecurrencePattern

        monkeypatch.setattr("builtins.input", lambda _: "1")
        recurrence = select_recurrence()
        assert recurrence == RecurrencePattern.DAILY

    def test_select_recurrence_weekly(self, monkeypatch):
        """Test selecting WEEKLY recurrence (option 2)."""
        from src.todo.cli import select_recurrence
        from src.todo.models import RecurrencePattern

        monkeypatch.setattr("builtins.input", lambda _: "2")
        recurrence = select_recurrence()
        assert recurrence == RecurrencePattern.WEEKLY

    def test_select_recurrence_biweekly(self, monkeypatch):
        """Test selecting BIWEEKLY recurrence (option 3)."""
        from src.todo.cli import select_recurrence
        from src.todo.models import RecurrencePattern

        monkeypatch.setattr("builtins.input", lambda _: "3")
        recurrence = select_recurrence()
        assert recurrence == RecurrencePattern.BIWEEKLY

    def test_select_recurrence_monthly(self, monkeypatch):
        """Test selecting MONTHLY recurrence (option 4)."""
        from src.todo.cli import select_recurrence
        from src.todo.models import RecurrencePattern

        monkeypatch.setattr("builtins.input", lambda _: "4")
        recurrence = select_recurrence()
        assert recurrence == RecurrencePattern.MONTHLY

    def test_select_recurrence_yearly(self, monkeypatch):
        """Test selecting YEARLY recurrence (option 5)."""
        from src.todo.cli import select_recurrence
        from src.todo.models import RecurrencePattern

        monkeypatch.setattr("builtins.input", lambda _: "5")
        recurrence = select_recurrence()
        assert recurrence == RecurrencePattern.YEARLY

    def test_select_recurrence_default_empty_input(self, monkeypatch):
        """Test that empty input returns None (no recurrence)."""
        from src.todo.cli import select_recurrence

        monkeypatch.setattr("builtins.input", lambda _: "")
        recurrence = select_recurrence()
        assert recurrence is None

    def test_select_recurrence_invalid_input(self, monkeypatch, capsys):
        """Test that invalid input returns None with error message."""
        from src.todo.cli import select_recurrence

        monkeypatch.setattr("builtins.input", lambda _: "99")
        recurrence = select_recurrence()
        assert recurrence is None

        captured = capsys.readouterr()
        assert "Invalid" in captured.out or "invalid" in captured.out

    def test_select_recurrence_invalid_text(self, monkeypatch, capsys):
        """Test that text input returns None with error message."""
        from src.todo.cli import select_recurrence

        monkeypatch.setattr("builtins.input", lambda _: "xyz")
        recurrence = select_recurrence()
        assert recurrence is None

        captured = capsys.readouterr()
        assert "Invalid" in captured.out or "invalid" in captured.out
