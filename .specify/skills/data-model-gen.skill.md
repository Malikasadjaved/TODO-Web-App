# Data Model Generator Agent Skill

## Purpose
Generate Python data models (Task class, enums) from feature specification and constitution requirements. Ensures data model aligns with all three tiers and includes proper type hints, validation, and docstrings.

## Parameters

### Required
- `feature` (string): Feature name to generate model for (e.g., "todo-core")

### Optional
- `output_file` (string): Where to write model (default: `src/todo/models.py`)
- `include_validation` (boolean): Add validation methods (default: true)
- `include_serialization` (boolean): Add to_dict/from_dict methods (default: true)

## Usage Examples

```bash
# Generate data model for todo-core feature
Skill: data-model-gen --feature todo-core

# Generate to custom location
Skill: data-model-gen --feature todo-core --output_file src/todo/core_models.py

# Generate minimal model (no validation/serialization)
Skill: data-model-gen --feature todo-core --include_validation false --include_serialization false
```

## Execution Steps

1. **Load Requirements**
   - Read `.specify/memory/constitution.md` for data model requirements:
     - Priority levels (HIGH, MEDIUM, LOW)
     - Tags/categories (Work, Home, custom)
     - Timestamps (created_date, due_date, completed_date)
     - Task types (scheduled, activity)
     - Recurrence patterns (DAILY, WEEKLY, MONTHLY, YEARLY)
     - Status (complete, incomplete)
   - Read `specs/<feature>/spec.md` for feature-specific fields
   - Read `specs/<feature>/data-model.md` if exists

2. **Generate Enums**
   ```python
   from enum import Enum
   from typing import Optional, List, Set
   from datetime import datetime

   class Priority(Enum):
       """Task priority levels."""
       HIGH = "HIGH"
       MEDIUM = "MEDIUM"
       LOW = "LOW"

   class TaskType(Enum):
       """Task type classification."""
       SCHEDULED = "scheduled"  # Has due date
       ACTIVITY = "activity"    # No due date, priority-based

   class RecurrencePattern(Enum):
       """Recurrence patterns for repeating tasks."""
       NONE = "none"
       DAILY = "daily"
       WEEKLY = "weekly"
       BIWEEKLY = "biweekly"
       MONTHLY = "monthly"
       YEARLY = "yearly"
   ```

3. **Generate Task Class**
   ```python
   class Task:
       """
       Represents a todo task with rich metadata.

       Attributes:
           id: Unique task identifier (auto-incremented)
           title: Task title (required)
           description: Detailed task description (optional)
           priority: Task priority (HIGH/MEDIUM/LOW, default MEDIUM)
           tags: Set of tags for categorization (Work, Home, custom)
           status: Completion status (complete/incomplete)
           task_type: SCHEDULED or ACTIVITY
           created_date: Timestamp when task was created
           due_date: Optional deadline for task completion
           completed_date: Timestamp when task was completed (if applicable)
           recurrence: Recurrence pattern for repeating tasks
       """

       def __init__(
           self,
           id: int,
           title: str,
           description: str = "",
           priority: Priority = Priority.MEDIUM,
           tags: Optional[Set[str]] = None,
           status: str = "incomplete",
           task_type: TaskType = TaskType.ACTIVITY,
           created_date: Optional[datetime] = None,
           due_date: Optional[datetime] = None,
           completed_date: Optional[datetime] = None,
           recurrence: RecurrencePattern = RecurrencePattern.NONE,
       ) -> None:
           """Initialize a new Task instance."""
           self.id = id
           self.title = title
           self.description = description
           self.priority = priority
           self.tags = tags or set()
           self.status = status
           self.task_type = task_type
           self.created_date = created_date or datetime.now()
           self.due_date = due_date
           self.completed_date = completed_date
           self.recurrence = recurrence

       [If include_validation=true:]
       def validate(self) -> None:
           """Validate task fields against business rules."""
           if not self.title or not self.title.strip():
               raise ValueError("Task title cannot be empty")
           if self.task_type == TaskType.SCHEDULED and not self.due_date:
               raise ValueError("Scheduled tasks must have a due date")
           if self.status not in ("complete", "incomplete"):
               raise ValueError("Status must be 'complete' or 'incomplete'")

       def is_overdue(self) -> bool:
           """Check if task is past its due date."""
           if not self.due_date or self.status == "complete":
               return False
           return datetime.now() > self.due_date

       [If include_serialization=true:]
       def to_dict(self) -> dict:
           """Convert task to dictionary for serialization."""
           return {
               "id": self.id,
               "title": self.title,
               "description": self.description,
               "priority": self.priority.value,
               "tags": list(self.tags),
               "status": self.status,
               "task_type": self.task_type.value,
               "created_date": self.created_date.isoformat(),
               "due_date": self.due_date.isoformat() if self.due_date else None,
               "completed_date": self.completed_date.isoformat() if self.completed_date else None,
               "recurrence": self.recurrence.value,
           }

       @classmethod
       def from_dict(cls, data: dict) -> "Task":
           """Create task from dictionary."""
           return cls(
               id=data["id"],
               title=data["title"],
               description=data.get("description", ""),
               priority=Priority(data.get("priority", "MEDIUM")),
               tags=set(data.get("tags", [])),
               status=data.get("status", "incomplete"),
               task_type=TaskType(data.get("task_type", "activity")),
               created_date=datetime.fromisoformat(data["created_date"]) if data.get("created_date") else None,
               due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
               completed_date=datetime.fromisoformat(data["completed_date"]) if data.get("completed_date") else None,
               recurrence=RecurrencePattern(data.get("recurrence", "none")),
           )

       def __repr__(self) -> str:
           """String representation for debugging."""
           return f"Task(id={self.id}, title='{self.title}', priority={self.priority.value}, status='{self.status}')"
   ```

4. **Add Header Comments**
   ```python
   """
   Data models for the Python CLI Todo Application.

   This module defines the core Task class and supporting enums (Priority, TaskType,
   RecurrencePattern) according to the project constitution requirements.

   Generated by: data-model-gen agent skill
   Feature: <feature>
   Generated: <ISO timestamp>
   Constitution version: <version from constitution.md>
   """
   ```

5. **Validate Generated Code**
   - Run mypy on generated file: `mypy <output_file> --strict`
   - Check for type errors
   - If errors found: Fix and re-validate
   - Run black formatter: `black <output_file>`

6. **Generate Test Stub**
   - Create `tests/test_models.py` with basic tests:
     ```python
     import pytest
     from datetime import datetime
     from src.todo.models import Task, Priority, TaskType, RecurrencePattern

     def test_task_creation():
         """Test creating a task with default values."""
         task = Task(id=1, title="Test task")
         assert task.id == 1
         assert task.title == "Test task"
         assert task.priority == Priority.MEDIUM
         assert task.status == "incomplete"

     def test_task_validation_empty_title():
         """Test validation fails for empty title."""
         task = Task(id=1, title="")
         with pytest.raises(ValueError, match="title cannot be empty"):
             task.validate()

     def test_task_is_overdue():
         """Test overdue detection."""
         past_date = datetime(2020, 1, 1)
         task = Task(id=1, title="Test", due_date=past_date)
         assert task.is_overdue() is True

     # Add more tests as needed...
     ```

7. **Generate Report**
   ```
   ==================== DATA MODEL GENERATOR REPORT ====================
   Feature: <feature>
   Output file: <output_file>
   Timestamp: <ISO datetime>

   [ENUMS GENERATED]
   ✅ Priority (3 values: HIGH, MEDIUM, LOW)
   ✅ TaskType (2 values: SCHEDULED, ACTIVITY)
   ✅ RecurrencePattern (6 values: NONE, DAILY, WEEKLY, BIWEEKLY, MONTHLY, YEARLY)

   [TASK CLASS]
   ✅ Fields: <count> (<field_names>)
   ✅ Type hints: All fields annotated
   ✅ Docstrings: Class and __init__ documented
   [If include_validation:] ✅ Validation: validate(), is_overdue()
   [If include_serialization:] ✅ Serialization: to_dict(), from_dict()

   [CODE QUALITY]
   ✅ Mypy validation: PASSED (strict mode)
   ✅ Black formatting: Applied
   ✅ Constitutional compliance: PASSED
     - Type hints: ✅
     - Docstrings: ✅
     - Line length ≤ 88: ✅

   [TEST STUB]
   ✅ Generated: tests/test_models.py
   Test cases: <count>

   [NEXT STEPS]
   1. Review generated model: <output_file>
   2. Extend tests in tests/test_models.py
   3. Run: pytest tests/test_models.py
   4. Integrate with storage.py and commands.py
   =====================================================================
   ```

8. **Exit Codes**
   - 0: Model generated successfully
   - 1: Validation failed (mypy errors)
   - 2: File write error

## Acceptance Criteria

- ✅ Generates all required enums (Priority, TaskType, RecurrencePattern)
- ✅ Generates Task class with all constitutional fields
- ✅ Includes complete type hints (Python 3.9+ syntax)
- ✅ Includes Google-style docstrings
- ✅ Optionally includes validation methods
- ✅ Optionally includes serialization methods
- ✅ Passes mypy strict mode validation
- ✅ Formatted with black
- ✅ Generates corresponding test stub

## Dependencies

- mypy
- black

## Error Handling

- **Feature not found**: "Error: Feature '<feature>' not found in specs/"
- **Output file exists**: "Warning: <output_file> exists. Overwrite? (y/n)"
- **Mypy validation failed**: "Error: Generated code has type errors. Review and fix."
- **Write permission denied**: "Error: Cannot write to <output_file>. Check permissions."

## Notes

- Review generated code before integrating - this is a starting point
- Extend validation logic based on feature-specific requirements
- Generated test stub covers basics; add comprehensive tests for all scenarios
- Re-run skill if constitution data model requirements change
