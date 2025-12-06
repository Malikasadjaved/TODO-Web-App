---
description: "Run tests for a specific tier (primary, intermediate, advanced, or all)"
---

# Test Tier Command

Run tier-specific tests with coverage analysis.

## Usage

```bash
/test-tier primary
/test-tier intermediate
/test-tier advanced
/test-tier all
```

## What This Command Does

This command invokes the **test-runner agent skill** to execute pytest on tier-specific test files with coverage analysis. It ensures that the tier meets the constitutional requirement of ≥85% test coverage.

## Execution

When you run this command, I will:

1. Validate the tier argument (must be: primary, intermediate, advanced, or all)
2. Invoke the test-runner skill with the specified tier
3. Run pytest on tier-specific test files:
   - **primary**: `tests/test_models.py`, `tests/test_storage.py`, `tests/test_commands.py` (CRUD operations)
   - **intermediate**: `tests/test_filters.py` (search, filter, sort)
   - **advanced**: `tests/test_scheduler.py`, `tests/test_notifications.py` (recurring tasks, reminders)
   - **all**: All test files
4. Generate coverage report (terminal + HTML)
5. Report results with pass/fail counts, coverage percentage, and specific failures

## Expected Output

```
==================== TEST RUNNER REPORT ====================
Tier: primary
Tests Run: 47
Passed: 47 ✅
Failed: 0 ❌
Skipped: 0 ⚠️
Coverage: 92% (Threshold: 85%)

HTML Coverage Report: htmlcov/index.html
===========================================================
```

## Arguments

- `$ARGUMENTS`: The tier to test (required)
  - Valid values: `primary`, `intermediate`, `advanced`, `all`

## Exit Codes

- 0: All tests passed, coverage ≥85%
- 1: Tests failed
- 2: Coverage below 85%
- 3: Tests passed but coverage below 85%

## Constitutional Compliance

This command enforces:
- **Principle VI (Test-First Development)**: Test coverage MUST be ≥85%
- **Three-Tier Architecture**: Tests organized by tier for independent validation

## Examples

### Test only primary tier
```bash
/test-tier primary
```

### Test all tiers
```bash
/test-tier all
```

## Related Commands

- `/coverage` - Generate detailed coverage report
- `/validate-tier` - Validate tier completion (includes testing)
- `/build` - Run full build including all tests
