---
description: "Verify tier completion against constitution requirements"
---

# Validate-Tier Command

Comprehensive validation that a tier (primary, intermediate, or advanced) is complete and ready for delivery.

## Usage

```bash
/validate-tier primary
/validate-tier intermediate
/validate-tier advanced
```

## What This Command Does

This command performs end-to-end validation of a tier against ALL constitutional requirements:

1. Feature completeness (all tier features implemented)
2. Code quality (linting, type checking, complexity)
3. Test coverage (≥85% for tier modules)
4. Task completion (all tasks in tasks.md marked done)
5. Documentation (docstrings, README updated)

## Execution

When you run this command, I will:

### **Step 1: Load Tier Definition**
- Read constitution for tier feature list
- Read `specs/<feature>/tasks.md` for tier-specific tasks
- Identify expected modules and files

### **Step 2: Validate Feature Completeness**
For each feature in the tier, check:
- ✅ Implementation file exists
- ✅ Feature function/class defined
- ✅ Feature accessible from CLI menu
- ✅ Basic functionality works (smoke test)

**PRIMARY TIER**:
- `add_task()` in commands.py
- `view_tasks()` in commands.py
- `update_task()` in commands.py
- `delete_task()` in commands.py
- `mark_complete()` in commands.py

**INTERMEDIATE TIER**:
- `search_tasks()` in filters.py
- `filter_tasks()` in filters.py
- `sort_tasks()` in filters.py
- Priority/tag support in models.py

**ADVANCED TIER**:
- `create_recurring_task()` in scheduler.py
- `schedule_reminder()` in notifications.py
- Recurrence calculation logic
- Notification delivery system

### **Step 3: Run Code Quality Checks**
- Invoke `/lint-all` on tier-specific modules
- Require Grade A or B (no critical issues)
- Check constitutional compliance:
  - Functions ≤ 50 lines
  - Files ≤ 500 lines
  - Type hints present
  - Docstrings present

### **Step 4: Run Tier Tests**
- Invoke `/test-tier <tier>`
- Verify all tests pass
- Verify coverage ≥85% for tier modules
- Check no skipped tests

### **Step 5: Validate Task Completion**
- Read `specs/<feature>/tasks.md`
- For each task in tier:
  - Check marked as complete (✅ or [x])
  - Invoke task-validator skill if not marked
  - Verify acceptance criteria met

### **Step 6: Validate Documentation**
- Check README.md mentions tier features
- Check all tier modules have docstrings
- Check tier features in CLI help text
- Verify usage examples present

### **Step 7: Integration Test (Manual)**
- Prompt user to test tier features interactively
- Guide through each feature
- Confirm all work as expected

## Expected Output

```
==================== TIER VALIDATION REPORT ====================
Tier: Primary
Feature: todo-core
Timestamp: 2025-12-06T04:00:00

[STEP 1/7: FEATURE COMPLETENESS]
✅ Feature implementations: 5/5
  ✅ add_task (commands.py:15)
  ✅ view_tasks (commands.py:45)
  ✅ update_task (commands.py:78)
  ✅ delete_task (commands.py:112)
  ✅ mark_complete (commands.py:134)

[STEP 2/7: CODE QUALITY]
✅ Quality grade: A
✅ Linting: PASSED (0 errors)
✅ Type checking: PASSED (0 errors)
✅ Complexity: PASSED (max function 42 lines, max file 287 lines)

[STEP 3/7: TIER TESTS]
✅ Tests run: 47
✅ Tests passed: 47 (100%)
✅ Tests failed: 0
✅ Coverage: 92% (≥85% required)

[STEP 4/7: TASK COMPLETION]
✅ Tasks completed: 12/12
  ✅ T1.1: Implement Task model
  ✅ T1.2: Implement TaskStorage
  ✅ T1.3: Implement add_task command
  ... (9 more)

[STEP 5/7: DOCUMENTATION]
✅ README.md: Tier features documented
✅ Module docstrings: All present
✅ Function docstrings: All public APIs documented
✅ CLI help text: Tier features listed

[STEP 6/7: INTEGRATION TEST]
Please test the following features interactively:

1. Add a new task
   → Run: python main.py
   → Choose: 1 (Primary Tier) → 1 (Add Task)
   → Enter title, priority, tags
   → Confirm: Was task created successfully? (y/n): y ✅

2. View all tasks
   → Choose: 1 (Primary Tier) → 2 (View Tasks)
   → Confirm: Are tasks displayed correctly? (y/n): y ✅

... (3 more features)

All integration tests passed ✅

[OVERALL VALIDATION]
✅ TIER VALIDATION: PASSED

Primary Tier is COMPLETE and ready for delivery.
All constitutional requirements met.

[NEXT STEPS]
- Create git commit: git commit -m "feat(primary): complete primary tier"
- Proceed to intermediate tier development
- Or: Create release tag for primary tier MVP
================================================================
```

## With Failures

If validation fails:

```
==================== TIER VALIDATION REPORT ====================
Tier: Intermediate
Feature: search-filter

[STEP 3/7: TIER TESTS]
❌ Tests failed: 3
Failed tests:
- tests/test_filters.py::test_search_case_insensitive
- tests/test_filters.py::test_filter_by_multiple_tags
- tests/test_filters.py::test_sort_by_priority_descending

[STEP 4/7: TASK COMPLETION]
❌ Tasks incomplete: 2/8
  ✅ T2.1: Implement search function
  ❌ T2.2: Implement filter by status (NOT MARKED COMPLETE)
  ❌ T2.3: Implement filter by priority (NOT MARKED COMPLETE)
  ... (5 more)

[OVERALL VALIDATION]
❌ TIER VALIDATION: FAILED

Intermediate Tier is INCOMPLETE.

[BLOCKERS]
1. Fix 3 failing tests in test_filters.py
2. Complete tasks T2.2 and T2.3
3. Mark completed tasks in specs/search-filter/tasks.md

[REMEDIATION STEPS]
1. Run: /test-tier intermediate --verbose
2. Debug and fix failing tests
3. Complete implementation for T2.2 and T2.3
4. Update tasks.md to mark T2.2, T2.3 complete
5. Re-run: /validate-tier intermediate
================================================================
```

## Arguments

- `$ARGUMENTS`: The tier to validate (required)
  - Valid values: `primary`, `intermediate`, `advanced`

## Exit Codes

- 0: Tier validation PASSED (all requirements met)
- 1: Feature completeness issues (missing implementations)
- 2: Code quality issues (linting, type errors, complexity)
- 3: Test failures or coverage below threshold
- 4: Task completion issues (tasks not done)
- 5: Documentation issues
- 6: Integration test failures

## Constitutional Compliance

This command enforces ALL constitutional requirements for tier completion:

- **Principle III (Three-Tier Architecture)**: All tier features implemented
- **Principle I (Clean Code)**: Quality checks, complexity limits
- **Principle VI (Test-First Development)**: Tests pass, coverage ≥85%
- **Principle VII (User Experience)**: Integration testing confirms UX

Per the constitution:
> "Tier completion: Each tier must be fully functional before next tier begins"

This command gates tier transitions.

## When to Run This Command

- **Before starting next tier**: Validate current tier complete
- **Before creating release**: Ensure tier ready for delivery
- **Before pull request**: Verify constitutional compliance
- **During code review**: Independent validation

## Tier Transition Workflow

```
1. Develop Primary Tier
2. Run: /validate-tier primary
3. If PASSED → Proceed to Intermediate Tier
4. If FAILED → Fix blockers, re-run validation
5. Repeat for Intermediate and Advanced tiers
```

## Related Commands

- `/test-tier <tier>` - Run only tier tests
- `/lint-all` - Run only code quality checks
- `/build` - Run full build (all tiers)
- `/coverage` - Detailed coverage analysis

## Notes

- This is the MOST COMPREHENSIVE validation command
- Integrates all other skills and commands
- Manual integration testing ensures real-world usability
- Constitutional gatekeeper for tier transitions
- Passing validation = tier ready for production
