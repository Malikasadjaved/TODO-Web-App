"""Tests for reminder notification system."""

from datetime import datetime, timedelta

import pytest

from src.todo.models import Task, Reminder
from src.todo import notifications


class TestReminderModel:
    """Test Reminder dataclass."""

    def test_reminder_dataclass(self):
        """Test creating Reminder instance."""
        reminder_time = datetime(2025, 12, 10, 13, 0)
        reminder = Reminder(
            task_id=1,
            reminder_time=reminder_time,
            status="pending",
            notification_message="Task due in 1 hour",
        )

        assert reminder.task_id == 1
        assert reminder.reminder_time == reminder_time
        assert reminder.status == "pending"
        assert reminder.notification_message == "Task due in 1 hour"

    def test_reminder_requires_due_date(self):
        """Test that tasks with reminders must have due dates."""
        # Task with reminder but no due date should fail validation
        with pytest.raises(ValueError, match="Reminder requires due date"):
            Task(id=1, title="Task", reminder_offset=2.0, due_date=None)


class TestParseReminderOffset:
    """Test parsing reminder offset."""

    def test_parse_reminder_offset(self):
        """Test parsing reminder offset from string."""
        from src.todo.commands import parse_reminder_offset

        # Valid offsets
        assert parse_reminder_offset("1.0") == 1.0
        assert parse_reminder_offset("2.5") == 2.5
        assert parse_reminder_offset("24") == 24.0

        # Invalid offsets
        assert parse_reminder_offset("invalid") is None
        assert parse_reminder_offset("") is None


class TestCalculateReminderTime:
    """Test reminder time calculation."""

    def test_calculate_reminder_time(self):
        """Test calculating reminder time from due date and offset."""
        due_date = datetime(2025, 12, 10, 14, 0)
        offset_hours = 1.0

        reminder_time = notifications.calculate_reminder_time(due_date, offset_hours)

        expected = datetime(2025, 12, 10, 13, 0)
        assert reminder_time == expected

    def test_calculate_reminder_time_multiple_hours(self):
        """Test reminder time with multiple hour offset."""
        due_date = datetime(2025, 12, 10, 14, 0)
        offset_hours = 24.0

        reminder_time = notifications.calculate_reminder_time(due_date, offset_hours)

        expected = datetime(2025, 12, 9, 14, 0)
        assert reminder_time == expected


class TestCheckReminders:
    """Test checking if reminders should trigger."""

    def test_check_reminder_should_trigger(self):
        """Test that reminder triggers when time has passed."""
        now = datetime.now()
        past_time = now - timedelta(minutes=5)

        reminder = Reminder(
            task_id=1,
            reminder_time=past_time,
            status="pending",
            notification_message="Test",
        )

        should_trigger = notifications.should_trigger_reminder(reminder, now)
        assert should_trigger is True

    def test_check_reminder_should_not_trigger_future(self):
        """Test that reminder doesn't trigger for future time."""
        now = datetime.now()
        future_time = now + timedelta(minutes=5)

        reminder = Reminder(
            task_id=1,
            reminder_time=future_time,
            status="pending",
            notification_message="Test",
        )

        should_trigger = notifications.should_trigger_reminder(reminder, now)
        assert should_trigger is False

    def test_check_reminder_already_triggered(self):
        """Test that triggered reminders don't trigger again."""
        now = datetime.now()
        past_time = now - timedelta(minutes=5)

        reminder = Reminder(
            task_id=1,
            reminder_time=past_time,
            status="triggered",  # Already triggered
            notification_message="Test",
        )

        should_trigger = notifications.should_trigger_reminder(reminder, now)
        assert should_trigger is False


class TestFormatNotificationMessage:
    """Test notification message formatting."""

    def test_format_notification_message(self):
        """Test formatting notification message for task."""
        task = Task(
            id=1,
            title="Team meeting",
            due_date=datetime(2025, 12, 10, 14, 0),
        )

        message = notifications.format_notification_message(task)

        assert "Team meeting" in message
        assert "2025-12-10 14:00" in message or "14:00" in message
