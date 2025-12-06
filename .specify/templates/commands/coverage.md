---
description: "Generate detailed test coverage report with missing line analysis"
---

# Coverage Command

Generate comprehensive test coverage report with HTML visualization and missing line identification.

## Usage

```bash
/coverage
```

## What This Command Does

This command generates a detailed test coverage analysis showing:
- Overall coverage percentage
- Coverage per module
- Missing lines (not covered by tests)
- HTML report for visual inspection

## Execution

When you run this command, I will:

1. **Run Tests with Coverage**
   ```bash
   pytest tests/ \
     --cov=src/todo \
     --cov-report=term-missing \
     --cov-report=html \
     --cov-report=json
   ```

2. **Parse Coverage Data**
   - Read coverage.json for detailed metrics
   - Identify modules below 85% threshold
   - List specific uncovered lines

3. **Generate Visual Report**
   - Create HTML report in `htmlcov/`
   - Highlight uncovered lines in source files
   - Provide clickable navigation

4. **Display Summary**
   - Overall coverage percentage
   - Per-module breakdown
   - Files needing attention
   - Path to HTML report

## Expected Output

```
==================== COVERAGE REPORT ====================
Timestamp: 2025-12-06T03:15:42
Total Coverage: 89%

[MODULE BREAKDOWN]
src/todo/models.py          95%  (missing: 45, 67-70)
src/todo/storage.py         91%  (missing: 102-105)
src/todo/commands.py        87%  (missing: 234-240, 256)
src/todo/filters.py         88%  (missing: 78, 120-125)
src/todo/scheduler.py       82%  ⚠️  BELOW THRESHOLD
  Missing lines: 45-52, 89-95, 134-140
src/todo/notifications.py   80%  ⚠️  BELOW THRESHOLD
  Missing lines: 23-30, 56-62, 78-85

[FILES BELOW 85% THRESHOLD]
⚠️  src/todo/scheduler.py: 82% (-3% from threshold)
  Recommendation: Add tests for edge cases in recurrence calculation

⚠️  src/todo/notifications.py: 80% (-5% from threshold)
  Recommendation: Add tests for notification delivery and error handling

[OVERALL STATUS]
✅ Total coverage: 89% (≥85% required)
⚠️  2 modules below threshold (need improvement)

HTML Report: file:///path/to/htmlcov/index.html
Open in browser to see detailed line-by-line coverage
=========================================================
```

## Arguments

None (analyzes entire codebase)

## Exit Codes

- 0: Coverage meets threshold (≥85%)
- 1: Overall coverage below threshold
- 2: One or more modules significantly below threshold (≥10% below)

## Constitutional Compliance

This command enforces:
- **Principle VI (Test-First Development)**: Test coverage MUST be ≥85%

## HTML Report Features

The generated HTML report (`htmlcov/index.html`) includes:
- **Index page**: Overall statistics and module list
- **Per-file pages**: Source code with color-coded coverage
  - Green: Covered lines
  - Red: Uncovered lines
  - Gray: Excluded/non-executable lines
- **Search**: Find specific functions/classes
- **Filtering**: Show only uncovered code

## Improving Coverage

For modules below threshold, follow these steps:

1. **Open HTML report** for the specific module
2. **Review uncovered lines** (highlighted in red)
3. **Identify missing test scenarios**:
   - Error paths not tested
   - Edge cases not covered
   - Exception handling not triggered
4. **Write tests** for uncovered scenarios
5. **Re-run coverage** to verify improvement

### Example: Improving scheduler.py coverage

```
Uncovered lines 45-52: Recurrence calculation for leap years
→ Add test: test_recurrence_leap_year_boundary()

Uncovered lines 89-95: End date validation for recurring tasks
→ Add test: test_recurring_task_with_end_date()

Uncovered lines 134-140: Error handling for invalid pattern
→ Add test: test_invalid_recurrence_pattern_raises_error()
```

## When to Run This Command

- After writing new tests
- Before completing a tier
- When coverage drops below threshold
- Before creating a pull request
- As part of code review process

## Related Commands

- `/test-tier <tier>` - Run tests for specific tier (includes coverage)
- `/build` - Full build including coverage check
- `/validate-tier <tier>` - Validate tier completion (checks coverage)

## Notes

- Coverage data saved to `.coverage` (SQLite database)
- HTML report regenerated each run (overwrites previous)
- Use `--cov-report=xml` for CI/CD integration (not included by default)
- "Missing lines" are line numbers in the source file not executed during tests
