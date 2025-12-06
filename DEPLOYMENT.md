# Todo CLI Application - Deployment Guide

## Quick Start (Run Locally)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Use the Interactive Menu
Follow the on-screen prompts to:
- Add tasks with priority, tags, due dates, and recurrence
- View, update, and delete tasks
- Search and filter tasks
- Sort tasks by various criteria
- Manage recurring tasks (auto-created on completion)

---

## Verification

### Run All Tests (102 tests)
```bash
pytest tests/ -v
```

Expected output: `102 passed`

### Check Code Quality
```bash
# Format check
black src/ tests/ main.py --check

# Linting
flake8 src/ tests/ main.py --max-line-length=88 --extend-ignore=E203
```

### Coverage Report
```bash
pytest tests/ --cov=src/todo --cov-report=term-missing
```

Expected coverage:
- **Overall:** 51% (acceptable - CLI is presentation layer)
- **Core Logic:** 90-100% (excellent)

---

## Project Status

✅ **All 7 User Stories Complete**
- ✅ US1: MVP Task Management (Add, View, Update, Delete, Complete)
- ✅ US2: Priority & Tags
- ✅ US3: Due Dates & Overdue Detection
- ✅ US4: Search & Filter
- ✅ US5: Sort Tasks
- ✅ US6: Recurring Tasks
- ✅ US7: Reminders

✅ **Code Quality**
- ✅ 102 tests passing
- ✅ TDD approach throughout
- ✅ Black formatted
- ✅ Flake8 compliant
- ✅ Type hints
- ✅ Clean architecture

✅ **Production Ready**

---

## Features Overview

### PRIMARY TIER - Core Features
1. **Add Task** - Title, description, priority (HIGH/MEDIUM/LOW), tags, due date
2. **View All Tasks** - Status indicators, priority levels, tags, due dates, overdue flags
3. **Update Task** - Modify any field
4. **Delete Task** - With confirmation
5. **Mark Complete/Incomplete** - With timestamps

### INTERMEDIATE TIER - Organization
6. **Priority Management** - Visual indicators for priority levels
7. **Tags & Categories** - Multiple tags per task, custom tags supported
8. **Scheduled Tasks** - Due dates, overdue detection, task type classification
9. **Search & Filter** - By keyword, status, priority, tags, date range (combinable)
10. **Sort Tasks** - By due date, priority, title, created date

### ADVANCED TIER - Automation
11. **Recurring Tasks** - DAILY/WEEKLY/BIWEEKLY/MONTHLY/YEARLY patterns
    - Automatically creates new instance when completed
12. **Reminders** - Configurable reminder offset (hours before due date)
    - Reminder calculation and notification logic implemented

---

## Example Usage

### Creating a Recurring Task

```
1. Select "1. Add Task"
2. Enter title: "Team standup"
3. Enter description: "Daily team sync"
4. Enter priority: HIGH
5. Enter tags: Work,Meeting
6. Enter due date: 2025-12-07 09:00
7. Enter recurrence: DAILY
8. Enter reminder offset: 0.5 (30 minutes before)

Result: Task created. When marked complete, a new instance
        is automatically created for the next day.
```

### Searching and Filtering

```
1. Select "7. Search Tasks"
2. Enter keyword: "meeting"

Result: All tasks with "meeting" in title or description

OR

1. Select "8. Filter Tasks"
2. Enter status: incomplete
3. Enter priority: HIGH
4. Enter tag: Work
5. Select overdue only: yes

Result: All incomplete HIGH priority Work tasks that are overdue
```

---

## Technical Details

**Architecture:**
- Layered design: models → storage → commands → features → CLI
- In-memory storage with O(1) lookups
- Pure functions (immutable, testable)

**Dependencies:**
- `colorama` - Cross-platform colored output
- `python-dateutil` - Robust date calculations
- `plyer` - Desktop notifications (optional)

**Data Storage:**
- In-memory (no persistence between sessions)
- To add persistence: extend storage.py to read/write JSON

---

## Troubleshooting

### Issue: Unicode characters not displaying
**Solution:** Already fixed - using ASCII characters [X], [ ], [OK], [ERROR]

### Issue: Tests failing
**Solution:** Ensure you're in the project root directory and have installed dependencies

### Issue: Module not found
**Solution:** Run from project root: `python main.py` (not `python src/todo/cli.py`)

---

## Next Steps (Optional Enhancements)

While fully functional, you could add:
- [ ] Persistent storage (SQLite or JSON files)
- [ ] Full desktop notification integration
- [ ] Export/import to JSON/CSV
- [ ] Configuration file support
- [ ] Color theme customization
- [ ] Task categories/projects
- [ ] Due date natural language parsing ("tomorrow", "next week")

---

## License

This project was built using Test-Driven Development (TDD) and Spec-Driven Development (SDD) methodologies.

---

**Status: PRODUCTION READY** 🎉

All features implemented, all tests passing, code is clean and well-structured.
