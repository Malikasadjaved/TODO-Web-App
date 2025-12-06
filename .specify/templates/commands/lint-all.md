---
description: "Run all linters and formatters (black, flake8, mypy) on the codebase"
---

# Lint-All Command

Run all code quality tools: black (formatter), flake8 (linter), and mypy (type checker).

## Usage

```bash
/lint-all
```

## What This Command Does

This command invokes the **code-analyzer agent skill** to run all constitutional code quality checks without running tests. This is faster than `/build` for quick quality verification during development.

## Execution

When you run this command, I will:

1. **Step 1: Black (Code Formatter)**
   - Check code formatting (line length 88)
   - Report files that would be reformatted
   - Optionally auto-fix with `--fix` flag

2. **Step 2: Flake8 (Linter)**
   - Check PEP 8 compliance
   - Check code complexity (max 10)
   - Check for common errors
   - Ignore E203, W503 (black compatibility)

3. **Step 3: Mypy (Type Checker)**
   - Static type analysis in strict mode
   - Verify type hints on all functions
   - Check for type errors

4. **Step 4: Complexity Analysis**
   - Verify no functions > 50 lines
   - Verify no files > 500 lines
   - Report constitutional violations

5. **Generate Report**
   - Quality grade (A-F)
   - Specific issues with line numbers
   - Actionable remediation steps

## Expected Output

```
==================== CODE ANALYZER REPORT ====================
Target: src/
Timestamp: 2025-12-06T03:30:15

[BLACK - CODE FORMATTING]
✅ Status: PASSED
Files checked: 8
Would reformat: 0

[FLAKE8 - LINTING]
✅ Status: PASSED
Total errors: 0
Files with errors: 0

[MYPY - TYPE CHECKING]
✅ Status: PASSED
Files checked: 8
Type errors: 0

[COMPLEXITY ANALYSIS]
✅ Status: PASSED
Average function length: 18 lines
Constitutional violations: 0

[OVERALL QUALITY SCORE]
Grade: A

All checks passed. Code meets constitutional standards.
=============================================================
```

## With Errors

If issues are found:

```
==================== CODE ANALYZER REPORT ====================
[BLACK - CODE FORMATTING]
❌ Status: FAILED
Would reformat: 2 files
- src/todo/commands.py
- src/todo/filters.py

[FLAKE8 - LINTING]
❌ Status: FAILED
Total errors: 8
Top issues:
- E501: 5 occurrences (line too long)
- C901: 2 occurrences (function too complex)
- F401: 1 occurrence (unused import)

src/todo/commands.py:45:80: E501 line too long (95 > 88 characters)
src/todo/commands.py:120:1: C901 'handle_search' is too complex (12)
src/todo/filters.py:12:1: F401 'typing.Dict' imported but unused

[MYPY - TYPE CHECKING]
❌ Status: FAILED
Type errors: 3

src/todo/storage.py:67: error: Missing return statement
src/todo/commands.py:145: error: Argument 1 has incompatible type "str"; expected "Priority"
src/todo/filters.py:89: error: Cannot determine type of 'result'

[COMPLEXITY ANALYSIS]
❌ Status: FAILED
Constitutional violations:
- Functions > 50 lines: 1
  - src/todo/commands.py:handle_add_task (63 lines)

[OVERALL QUALITY SCORE]
Grade: D

[RECOMMENDATIONS]
1. Run black to auto-fix formatting: black src/ --line-length 88
2. Refactor handle_search() to reduce complexity (split into smaller functions)
3. Refactor handle_add_task() - currently 63 lines (max 50)
4. Add return type hint to function at storage.py:67
5. Fix type error at commands.py:145 (convert string to Priority enum)
6. Add type annotation for 'result' at filters.py:89
7. Remove unused import at filters.py:12
=============================================================
```

## Arguments

None (analyzes entire `src/` directory)

## Exit Codes

- 0: All checks passed (Grade A)
- 1: Formatting issues only (Grade B)
- 2: Linting or type errors (Grade C-D)
- 3: Critical violations (Grade F)

## Constitutional Compliance

This command enforces:

- **Principle I (Clean Code & Pythonic Design)**:
  - PEP 8 compliance
  - Type hints on all functions
  - Functions ≤ 50 lines
  - Files ≤ 500 lines
  - Descriptive naming

- **Code Quality Standards**:
  - Black formatting (line length 88)
  - Flake8 linting (complexity ≤10)
  - Mypy strict mode type checking

## Auto-Fix Mode

To automatically fix formatting issues:

```bash
/lint-all --fix
```

This will run `black src/` to reformat code. Review changes before committing.

## When to Run This Command

- **During development**: After making changes, before committing
- **Before tests**: Ensure code quality before running tests
- **Code review**: Verify constitutional compliance
- **CI/CD**: As pre-test quality gate

## Comparison with /build

| Feature | /lint-all | /build |
|---------|-----------|--------|
| Black | ✅ | ✅ |
| Flake8 | ✅ | ✅ |
| Mypy | ✅ | ✅ |
| Tests | ❌ | ✅ |
| Coverage | ❌ | ✅ |
| Speed | Fast (~10s) | Slower (~60s) |
| Use case | Quick quality check | Full validation |

## Related Commands

- `/build` - Full build including tests and coverage
- `/test-tier <tier>` - Run tests only
- `/validate-tier <tier>` - Validate tier completion

## Notes

- **Grade A**: Production-ready code, all checks passed
- **Grade B**: Minor formatting issues (auto-fixable)
- **Grade C**: Linting errors or few type errors (needs manual fixes)
- **Grade D**: Multiple type errors or complexity violations (significant work needed)
- **Grade F**: Critical issues across multiple categories (refactoring required)

Grade C or below is NOT acceptable for committing code per the constitution.
