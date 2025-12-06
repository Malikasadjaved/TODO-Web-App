<!--
Sync Impact Report:
- Version change: 2.0.0 → 2.1.0
- Reason: MINOR version bump - Added new core principle (VII. Reusable Intelligence)
- Previous changes: 1.0.0 → 2.0.0 (MAJOR) - Three-tier feature architecture expansion
- Modified principles:
  - Added VII. "Reusable Intelligence & Agent-Driven Development" (NEW)
  - Renumbered: IV → V (Python Project Structure), V → VI (Test-First Development), VI → VII (User Experience)
- Added sections:
  - Reusable Intelligence principle with subagent, slash command, agent skill, and MCP server requirements
  - Cloud-native blueprints and agent skill development mandate
  - .specify/skills/ directory structure for reusable agent skills
- Removed sections: None
- Templates requiring updates:
  - ⚠ .specify/templates/spec-template.md - Should reflect three-tier feature prioritization
  - ⚠ .specify/templates/plan-template.md - Should include enhanced data model and scheduling architecture
  - ⚠ .specify/templates/tasks-template.md - Should organize tasks by feature tier
  - ✅ Project structure updated to include .specify/skills/ directory
- Follow-up TODOs:
  - Create initial agent skills for common operations (test runner, code analyzer, builder)
  - Define custom slash commands for project-specific workflows
  - Consider whether notifications require external library (stdlib schedule vs APScheduler)
  - Decide on date/time library: stdlib datetime vs python-dateutil for recurrence
  - Evaluate if browser notifications require web interface or desktop notification library
-->

# Python CLI Todo Application Constitution

## Core Principles

### I. Clean Code & Pythonic Design

**All code MUST adhere to Python best practices and PEP 8 guidelines.**

- Follow PEP 8 style guide for naming conventions, indentation, and formatting
- Use type hints for function signatures and class attributes (Python 3.9+ syntax)
- Prefer composition over inheritance; keep class hierarchies shallow
- Functions should do one thing well; maintain single responsibility principle
- Use descriptive variable and function names that reveal intent
- Maximum function length: 50 lines; maximum file length: 500 lines
- Avoid magic numbers; use named constants or enums
- Document public APIs with Google-style or NumPy-style docstrings

**Rationale**: Clean, Pythonic code is easier to maintain, test, and extend. Type hints catch errors early and improve IDE support.

### II. Enhanced In-Memory Storage Architecture

**Task data MUST be stored exclusively in memory using Python data structures with support for rich metadata.**

- Use appropriate built-in data structures (lists, dicts, sets) for task storage
- Primary storage: List of Task objects or dictionaries with complete metadata
- Task IDs MUST be unique integers, auto-incremented
- No external database or file system persistence (in-memory only)
- Data structure MUST support O(1) or O(log n) lookups by ID
- All CRUD operations must maintain data integrity (no orphaned references)

**Enhanced data model requirements:**
- Priority levels: Enum or string constants (HIGH, MEDIUM, LOW)
- Tags/Categories: Set or list of strings (e.g., "Work", "Home", custom)
- Timestamps: created_date, due_date (optional), overdue flag (computed)
- Task types: "scheduled" (with due date) vs "activity" (priority-based, no deadline)
- Recurrence pattern: Optional string or enum (DAILY, WEEKLY, MONTHLY, etc.)
- Completion tracking: status (complete/incomplete), completed_date (optional)

**Rationale**: In-memory storage keeps the application fast and simple while supporting advanced organizational features through rich metadata.

### III. Three-Tier Feature Architecture (NON-NEGOTIABLE)

**The application MUST implement features across three progressive tiers: Primary, Intermediate, and Advanced.**

---

#### **PRIMARY TIER: Core CRUD Operations**

These foundational features are MANDATORY and form the minimum viable product:

1. **Add Task**: Create new task with title (required) and description (optional)
   - Auto-assign unique integer ID
   - Set initial status to "incomplete"
   - Optionally assign priority (HIGH/MEDIUM/LOW, default: MEDIUM)
   - Optionally add tags/categories (Work/Home or custom)
   - Optionally set due date and task type (scheduled vs activity)
   - Return confirmation with assigned ID

2. **View Task**: List all tasks with comprehensive status indicators
   - Display: ID, Title, Description (truncated if long), Status, Priority, Tags, Due Date
   - Visual status indicators: [✓] complete, [ ] incomplete
   - Priority indicators: [H] High, [M] Medium, [L] Low
   - Overdue indicator: [!] for tasks past due date
   - Support empty state message when no tasks exist

3. **Update Task**: Modify task details by ID
   - Allow updating title, description, priority, tags, due date, task type
   - Validate task ID exists before update
   - Preserve task ID, created date, and completion status during update
   - Provide field-specific update prompts

4. **Delete Task**: Remove task by ID
   - Validate task ID exists before deletion
   - Provide confirmation message with task details
   - Handle invalid ID gracefully
   - Confirm destructive action (y/n prompt)

5. **Mark Complete/Incomplete**: Toggle task completion status by ID
   - Support marking complete and marking incomplete
   - Record completion timestamp when marked complete
   - Validate task ID exists
   - Provide visual confirmation of status change

---

#### **INTERMEDIATE TIER: Organization & Usability**

These features enhance task management and organization:

6. **Priority Management**: Assign and update priority levels
   - Three levels: HIGH, MEDIUM, LOW
   - Visual indicators in task lists
   - Default priority: MEDIUM for new tasks
   - Validate priority values on input

7. **Tags & Categories**: Label and categorize tasks
   - Predefined categories: Work, Home
   - Support custom tags (user-defined strings)
   - Allow multiple tags per task
   - Display tags in task view with visual separators

8. **Scheduled Tasks**: Time-based task management
   - Created Date: Auto-set timestamp when task is created
   - Due Date: Optional user-specified deadline (date and optional time)
   - Overdue Detection: Auto-flag tasks past due date
   - Task Type: "scheduled" (with deadline) or "activity" (no deadline)

9. **Search & Filter**: Find and filter tasks by multiple criteria
   - **Search by Keyword**: Search in title and description (case-insensitive)
   - **Filter by Status**: Show only complete or incomplete tasks
   - **Filter by Priority**: Show tasks of specific priority level(s)
   - **Filter by Date**: Show tasks due today, this week, overdue, or by custom date range
   - **Filter by Tags**: Show tasks with specific tag(s)
   - Support combining multiple filters (AND logic)

10. **Sort Tasks**: Reorder task list by different criteria
    - Sort by Due Date (ascending/descending, nulls last)
    - Sort by Priority (HIGH → MEDIUM → LOW or reverse)
    - Sort Alphabetically by title (A-Z or Z-A)
    - Sort by Created Date (newest/oldest first)
    - Display current sort order to user

---

#### **ADVANCED TIER: Intelligent Features**

These features add automation and smart capabilities:

11. **Recurring Tasks**: Auto-reschedule repeating tasks
    - Recurrence patterns: DAILY, WEEKLY, BIWEEKLY, MONTHLY, YEARLY
    - Examples: "Weekly team meeting", "Monthly report"
    - Auto-create new task instance when current one is completed
    - Preserve title, description, priority, and tags in new instance
    - Calculate next due date based on recurrence pattern
    - Option to stop recurrence or set end date

12. **Due Date & Time Reminders**: Deadline notifications
    - Set due date with date picker (YYYY-MM-DD format)
    - Optional time component (HH:MM format, 24-hour)
    - Reminder notifications before due date/time (e.g., 1 hour, 1 day before)
    - Desktop notifications (OS-level) or in-app alerts
    - Browser notifications if web interface is added later
    - Display upcoming deadlines in dashboard view

---

**Rationale**: Three-tier architecture allows incremental development and delivery. Primary tier establishes MVP, Intermediate tier adds power-user features, Advanced tier provides intelligent automation. Each tier builds on the previous.

### IV. Reusable Intelligence & Agent-Driven Development

**Development MUST leverage Claude Code's agent capabilities to create reusable, composable intelligence.**

All developers and AI assistants working on this project MUST utilize Claude Code's advanced capabilities to build and reuse intelligent workflows, rather than manually repeating tasks or writing ad-hoc solutions.

**Mandatory capabilities:**

1. **Subagents for Complex Tasks**
   - Use Task tool with specialized subagent types for multi-step operations:
     - `Explore` agent: Codebase exploration, pattern discovery, architectural understanding
     - `Plan` agent: Implementation planning, architectural design decisions
     - `general-purpose` agent: Complex multi-step tasks requiring autonomous execution
   - Launch subagents in parallel when tasks are independent (performance optimization)
   - Prefer subagents over manual multi-step operations for consistency and auditability

2. **Custom Slash Commands**
   - Create project-specific slash commands in `.specify/templates/commands/`
   - Required commands to implement:
     - `/test-tier <primary|intermediate|advanced>`: Run tests for specific tier
     - `/build`: Build and validate entire application
     - `/coverage`: Generate test coverage report
     - `/lint-all`: Run black, flake8, mypy on entire codebase
     - `/validate-tier <tier>`: Verify tier completion against constitution requirements
   - Document each command with clear description, parameters, and usage examples
   - Commands MUST be idempotent and provide clear success/failure feedback

3. **Agent Skills & Cloud-Native Blueprints**
   - Develop reusable agent skills in `.specify/skills/` directory:
     - **Test Runner Skill**: Automated test execution with coverage analysis
     - **Code Analyzer Skill**: Static analysis, complexity metrics, code quality checks
     - **Task Validator Skill**: Verify task completion against acceptance criteria
     - **Data Model Generator Skill**: Generate Task class and enums from spec
     - **CLI Builder Skill**: Generate menu-driven CLI from feature spec
   - Skills MUST be:
     - Self-contained: Include all necessary context and instructions
     - Parameterized: Accept configuration for different contexts
     - Documented: Clear purpose, inputs, outputs, and usage examples
   - Create cloud-native blueprints for common patterns (CRUD operations, filtering, sorting)

4. **MCP Server Integration**
   - Integrate Model Context Protocol (MCP) servers for extended capabilities:
     - File system operations (if needed beyond standard tools)
     - External API integrations (e.g., notification services)
     - Database/storage adapters (if persistence added later)
   - Document MCP server configuration in `.claude/config.json` or equivalent
   - Prefer official or well-maintained MCP servers over custom implementations
   - Test MCP server integrations thoroughly (connectivity, error handling, fallbacks)

**Project structure for reusable intelligence:**
```
.specify/
├── skills/                      # Agent skills (reusable AI workflows)
│   ├── test-runner.skill.md
│   ├── code-analyzer.skill.md
│   ├── task-validator.skill.md
│   ├── data-model-gen.skill.md
│   └── cli-builder.skill.md
├── templates/
│   └── commands/                # Custom slash commands
│       ├── test-tier.md
│       ├── build.md
│       ├── coverage.md
│       ├── lint-all.md
│       └── validate-tier.md
└── blueprints/                  # Cloud-native code generation blueprints
    ├── crud-operations.blueprint.md
    ├── filter-sort.blueprint.md
    └── cli-menu.blueprint.md
```

**Development workflow integration:**
- Before manual implementation, check if an agent skill or blueprint exists
- Create new skills/blueprints when repeating similar tasks 3+ times
- Refactor manual workflows into skills after validation
- Share skills across features and tiers for consistency
- Version control all skills, commands, and blueprints alongside code

**Quality requirements:**
- Agent skills MUST have clear acceptance criteria and test cases
- Slash commands MUST handle errors gracefully and provide actionable feedback
- Blueprints MUST generate code that passes all quality gates (black, flake8, mypy, tests)
- All reusable intelligence artifacts MUST be documented in README.md

**Rationale**: Reusable intelligence eliminates repetitive manual work, ensures consistency across the codebase, captures institutional knowledge, and accelerates development. Agent-driven workflows are auditable, reproducible, and continuously improvable. Cloud-native blueprints enable rapid feature development while maintaining code quality standards.

### V. Proper Python Project Structure

**Project MUST follow standard Python package layout with clear module separation.**

Required structure:
```
todo-app/
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py          # Task data model (Task class, enums)
│       ├── storage.py         # In-memory storage manager (CRUD)
│       ├── commands.py        # Command handlers (add, delete, update, etc.)
│       ├── filters.py         # Search, filter, and sort logic
│       ├── scheduler.py       # Recurring tasks and reminders
│       ├── notifications.py   # Reminder and notification system
│       └── cli.py             # CLI interface and main loop
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_commands.py
│   ├── test_filters.py
│   ├── test_scheduler.py
│   ├── test_notifications.py
│   └── test_cli.py
├── .specify/                  # Spec-driven development artifacts
├── main.py                    # Entry point
├── requirements.txt
└── README.md
```

**Separation of concerns MUST be maintained:**
- `models.py`: Task class, Priority enum, TaskType enum, RecurrencePattern enum, validation
- `storage.py`: In-memory storage operations (CRUD, ID generation, data integrity)
- `commands.py`: Business logic for each feature (add, update, delete, complete, etc.)
- `filters.py`: Search, filter, and sort algorithms
- `scheduler.py`: Recurring task logic, next due date calculation
- `notifications.py`: Reminder system, notification delivery
- `cli.py`: User interface, menu system, input parsing, output formatting

**Rationale**: Proper structure with specialized modules makes the codebase navigable, testable, and maintainable. Clear separation enables independent development and testing of each tier.

### VI. Test-First Development (NON-NEGOTIABLE)

**All features MUST follow TDD: Write tests → Tests fail → Implement → Tests pass.**

- Unit tests required for all public functions and methods
- Test coverage MUST be ≥ 85% for core modules (models, storage, commands, filters, scheduler)
- Use `pytest` as the testing framework
- Tests MUST be isolated: no shared state between test cases
- Test file naming: `test_<module>.py`
- Test function naming: `test_<function>_<scenario>_<expected_result>`
- Edge cases MUST be tested: empty input, invalid IDs, boundary conditions, date edge cases
- Mock time-dependent functions (datetime.now, notification triggers)

**Red-Green-Refactor cycle:**
1. Write failing test that specifies desired behavior
2. Get user approval for test cases
3. Run tests → verify they fail
4. Implement minimal code to pass tests
5. Refactor for clean code principles
6. Repeat

**Additional test requirements for new features:**
- Priority tests: Validate all three levels, reject invalid values
- Tag tests: Multiple tags, special characters, empty tags
- Date tests: Valid/invalid formats, past dates, timezone handling, overdue detection
- Filter tests: Single criteria, combined filters, empty result sets
- Sort tests: Multiple sort keys, null handling, stability
- Recurrence tests: Pattern calculation, edge cases (leap years, month boundaries)
- Notification tests: Timing accuracy, multiple reminders, cancellation

**Rationale**: TDD ensures correctness, prevents regressions, and serves as living documentation. Comprehensive tests are critical for date/time logic and recurring task calculations.

### VII. Enhanced User Experience & Error Handling

**CLI MUST be intuitive, feature-rich, and provide excellent feedback.**

- Display clear menu with numbered options organized by feature tier
- Accept both numeric menu choices and command keywords (add, list, search, filter, sort, etc.)
- Validate all user input before processing (dates, priorities, tags, recurrence patterns)
- Display helpful error messages for invalid input (not Python tracebacks)
- Confirm destructive actions (delete, stop recurrence) with y/n prompt
- Support graceful exit (quit/exit command)
- Use colored output for priority levels, status, and errors (colorama library recommended)
- Provide usage examples and help text for complex features (search, filter, recurrence)

**Enhanced display requirements:**
- Task list views: Tabular format with columns (ID, Title, Priority, Tags, Due Date, Status)
- Color coding: Red (HIGH priority), Yellow (MEDIUM), Green (LOW), Gray (completed)
- Overdue tasks: Highlighted in red with [!] indicator
- Search/filter results: Show match count and applied criteria
- Sort indicator: Display current sort order in list header
- Notification display: Clear, non-intrusive alerts for upcoming deadlines

**Error handling requirements:**
- Catch and handle all exceptions; never crash with unhandled exception
- Invalid task IDs: "Error: Task with ID {id} not found."
- Invalid dates: "Error: Invalid date format. Use YYYY-MM-DD."
- Invalid priority: "Error: Priority must be HIGH, MEDIUM, or LOW."
- Invalid recurrence: "Error: Recurrence pattern must be DAILY, WEEKLY, MONTHLY, or YEARLY."
- Empty search: "No tasks found matching '{keyword}'."
- Empty filter: "No tasks match the selected criteria."

**Rationale**: Good UX makes complex features accessible. Clear feedback, validation, and color coding help users manage large task lists effectively. Robust error handling prevents frustration and data loss.

## Code Quality Standards

### Formatting & Linting
- Use `black` for code formatting (line length: 88)
- Use `flake8` for linting (ignore E203, W503 for black compatibility)
- Use `mypy` for static type checking (strict mode)
- All checks MUST pass before committing code

### Documentation
- README.md MUST include: setup instructions, usage examples for all three tiers, feature list
- Inline comments only for non-obvious logic (prefer self-documenting code)
- Docstrings required for all public classes, functions, and modules
- Document date formats, recurrence patterns, and notification behavior clearly

### Dependencies
- Minimize external dependencies; prefer standard library
- **Required**: pytest, black, flake8, mypy (dev dependencies)
- **Recommended**: colorama (colored terminal output)
- **Conditional**:
  - python-dateutil (for recurrence calculation, if stdlib insufficient)
  - plyer or desktop-notifier (for cross-platform notifications)
  - APScheduler (if advanced scheduling needed, evaluate vs stdlib)
- Document all dependencies in requirements.txt with version pins
- Justify any dependency beyond stdlib in ADR

## Development Workflow

### Feature Development Process
1. Create feature spec in `specs/<feature>/spec.md` organized by tier
2. Design architecture in `specs/<feature>/plan.md` with data model and contracts
3. Break down into tasks in `specs/<feature>/tasks.md` by tier (Primary → Intermediate → Advanced)
4. Develop in tier order: Complete Primary tier fully before Intermediate
5. Write tests for first task (Red phase)
6. Get user approval for tests
7. Implement feature (Green phase)
8. Refactor for clean code (Refactor phase)
9. Repeat for remaining tasks within tier
10. Create PHR (Prompt History Record) documenting the session

### Code Review Requirements
- All code changes MUST be reviewed against constitution principles
- Verify: PEP 8 compliance, type hints present, tests passing (≥85% coverage), documentation updated
- No code merged without passing all quality gates (black, flake8, mypy, pytest)
- Tier dependencies: Ensure no Advanced tier code depends on incomplete Intermediate features

### Git Workflow
- Commit messages: `<type>(<tier>): <description>` (e.g., `feat(primary): add task with priority`)
- Types: feat, fix, refactor, test, docs, chore
- Keep commits atomic and focused
- Branch naming: `feature/<tier>-<feature-name>` (e.g., `feature/intermediate-search-filter`)

## Governance

**This constitution supersedes all other development practices and serves as the authoritative source of truth for the Python CLI Todo Application project.**

### Amendment Procedure
- Amendments require: clear rationale, impact analysis, user approval
- Version bumps follow semantic versioning:
  - MAJOR: Breaking changes to principles, architecture, or tier redefinition
  - MINOR: New principle added, new tier introduced, or significant expansion
  - PATCH: Clarifications, typo fixes, non-semantic changes
- All amendments MUST update dependent templates (spec, plan, tasks)
- Amendment history tracked in Sync Impact Report (HTML comment at top of file)

### Compliance
- All PRs and code reviews MUST verify compliance with constitution principles
- Deviations MUST be explicitly justified and documented in ADR
- Complexity MUST be justified; simplicity preferred when equally effective
- Use `CLAUDE.md` for runtime development guidance and agent instructions
- Tier completion: Each tier must be fully functional before next tier begins

### Versioning & Dates
**Version**: 2.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
