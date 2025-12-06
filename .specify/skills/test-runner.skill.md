# Test Runner Agent Skill

## Purpose
Automated test execution with coverage analysis for the Python CLI Todo Application. This skill runs pytest with appropriate flags, analyzes coverage, and provides actionable feedback.

## Parameters

### Required
- `tier` (string): Which tier to test - `primary`, `intermediate`, `advanced`, or `all`

### Optional
- `coverage_threshold` (integer): Minimum coverage percentage required (default: 85)
- `verbose` (boolean): Show verbose test output (default: false)
- `fail_fast` (boolean): Stop on first test failure (default: false)

## Usage Examples

```bash
# Run all tests with coverage
Skill: test-runner --tier all

# Run only primary tier tests
Skill: test-runner --tier primary

# Run with verbose output and fail-fast
Skill: test-runner --tier intermediate --verbose true --fail_fast true
```

## Execution Steps

1. **Validate Environment**
   - Check that pytest is installed: `pytest --version`
   - Check that pytest-cov is installed: `pytest --cov --version`
   - Verify tests/ directory exists
   - If missing, report error and exit

2. **Determine Test Scope**
   - If `tier=primary`: Run tests in `tests/test_models.py`, `tests/test_storage.py`, `tests/test_commands.py` (CRUD only)
   - If `tier=intermediate`: Run tests in `tests/test_filters.py` (search, filter, sort)
   - If `tier=advanced`: Run tests in `tests/test_scheduler.py`, `tests/test_notifications.py`
   - If `tier=all`: Run all tests in `tests/`

3. **Execute pytest**
   ```bash
   pytest <test-files> \
     --cov=src/todo \
     --cov-report=term-missing \
     --cov-report=html \
     --cov-fail-under=<coverage_threshold> \
     [--verbose] \
     [--exitfirst]
   ```

4. **Analyze Results**
   - Parse pytest output for:
     - Total tests run
     - Passed count
     - Failed count
     - Skipped count
     - Coverage percentage
   - If coverage < threshold: Report specific modules below threshold
   - If tests failed: List failed test names and assertion errors

5. **Generate Report**
   ```
   ==================== TEST RUNNER REPORT ====================
   Tier: <tier>
   Tests Run: <count>
   Passed: <count> ✅
   Failed: <count> ❌
   Skipped: <count> ⚠️
   Coverage: <percentage>% (Threshold: <threshold>%)

   [If failed tests exist:]
   Failed Tests:
   - <test_file>::<test_function>: <error_summary>

   [If coverage below threshold:]
   Coverage Gaps:
   - <module_name>: <percentage>% (missing lines: <line_numbers>)

   HTML Coverage Report: htmlcov/index.html
   ===========================================================
   ```

6. **Exit Codes**
   - 0: All tests passed, coverage met
   - 1: Tests failed
   - 2: Coverage below threshold
   - 3: Tests passed but coverage below threshold

## Acceptance Criteria

- ✅ Runs pytest with correct test scope based on tier
- ✅ Generates coverage report (terminal + HTML)
- ✅ Enforces coverage threshold (default 85%)
- ✅ Provides clear, actionable error messages for failures
- ✅ Lists specific failed tests with error summaries
- ✅ Identifies modules below coverage threshold with missing line numbers
- ✅ Returns appropriate exit code for automation

## Dependencies

- pytest
- pytest-cov

## Error Handling

- **pytest not installed**: "Error: pytest not found. Run: pip install pytest pytest-cov"
- **tests/ directory missing**: "Error: tests/ directory not found. Create test files first."
- **Invalid tier**: "Error: tier must be 'primary', 'intermediate', 'advanced', or 'all'"
- **No tests found for tier**: "Warning: No test files found for tier '<tier>'. Skipping."

## Notes

- This skill is idempotent: can run multiple times safely
- HTML coverage report saved to `htmlcov/` directory
- Use `--verbose` for debugging test failures
- Use `--fail_fast` for rapid iteration during development
