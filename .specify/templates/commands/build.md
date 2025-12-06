---
description: "Build and validate the entire application (linting, type checking, tests)"
---

# Build Command

Run complete build process: code analysis, type checking, and all tests.

## Usage

```bash
/build
```

## What This Command Does

This command runs a full build pipeline to ensure the application meets all constitutional quality standards:

1. **Code Analysis** - Run black, flake8, mypy (via code-analyzer skill)
2. **Test Execution** - Run all tests with coverage (via test-runner skill)
3. **Validation** - Verify constitutional compliance

This is the equivalent of a CI/CD build pipeline run locally.

## Execution

When you run this command, I will:

1. **Step 1: Code Analysis**
   - Invoke code-analyzer skill on `src/`
   - Check black formatting (line length 88)
   - Check flake8 linting (complexity ≤10, ignore E203/W503)
   - Check mypy type checking (strict mode)
   - Report quality grade (A-F)

2. **Step 2: Test Execution**
   - Invoke test-runner skill with `tier=all`
   - Run all tests in `tests/`
   - Generate coverage report
   - Verify coverage ≥85%

3. **Step 3: Constitutional Compliance**
   - Verify no functions > 50 lines
   - Verify no files > 500 lines
   - Check all quality gates passed

4. **Step 4: Build Report**
   - Summarize results from all steps
   - Overall build status: PASSED or FAILED
   - List any failures with remediation steps

## Expected Output

```
==================== BUILD REPORT ====================
Timestamp: 2025-12-06T02:45:30

[STEP 1/3: CODE ANALYSIS]
✅ Black formatting: PASSED (0 files need reformatting)
✅ Flake8 linting: PASSED (0 errors)
✅ Mypy type checking: PASSED (0 type errors)
✅ Code quality grade: A

[STEP 2/3: TEST EXECUTION]
✅ Tests run: 152
✅ Tests passed: 152
✅ Tests failed: 0
✅ Coverage: 89% (≥85% required)

[STEP 3/3: CONSTITUTIONAL COMPLIANCE]
✅ Function length: All ≤50 lines
✅ File length: All ≤500 lines
✅ Type hints: Present on all public APIs
✅ Docstrings: Present on all public APIs

[BUILD STATUS]
✅ BUILD PASSED

All quality gates passed. Application ready for deployment.
======================================================
```

## Arguments

None (builds entire application)

## Exit Codes

- 0: Build passed (all quality gates)
- 1: Code analysis failed (formatting, linting, or type errors)
- 2: Tests failed
- 3: Coverage below threshold
- 4: Constitutional violations (function/file length)

## Constitutional Compliance

This command enforces ALL constitutional quality standards:

- **Principle I (Clean Code)**: PEP 8, type hints, function/file length limits
- **Principle VI (Test-First Development)**: ≥85% coverage
- **Code Quality Standards**: black, flake8, mypy all passing

## Build Failures

If the build fails, I will provide specific remediation steps:

**Code Analysis Failures:**
```
❌ Code Analysis Failed (Grade C)
Issues found:
- Flake8: 12 errors (complexity violations in src/todo/commands.py)
- Mypy: 3 type errors (missing return types)

Remediation:
1. Run: black src/ --line-length 88
2. Fix complexity: Refactor functions in src/todo/commands.py
3. Add type hints: See mypy errors above
4. Re-run: /build
```

**Test Failures:**
```
❌ Tests Failed (5 failures)
Failed tests:
- tests/test_filters.py::test_search_by_keyword
- tests/test_filters.py::test_filter_by_priority

Remediation:
1. Review failed tests above
2. Fix implementation or update tests
3. Re-run: /test-tier intermediate
4. Then re-run: /build
```

## When to Run This Command

- Before committing code
- Before creating a pull request
- After completing a tier
- Before deployment
- As part of CI/CD pipeline

## Related Commands

- `/lint-all` - Run only code analysis (faster for quick checks)
- `/test-tier` - Run tests for specific tier
- `/coverage` - Generate detailed coverage report
- `/validate-tier` - Validate tier completion including build
