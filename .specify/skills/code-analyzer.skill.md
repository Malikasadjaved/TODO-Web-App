# Code Analyzer Agent Skill

## Purpose
Static analysis, complexity metrics, and code quality checks for the Python CLI Todo Application. Runs black, flake8, mypy, and analyzes code complexity to ensure constitutional compliance.

## Parameters

### Required
None (analyzes entire codebase by default)

### Optional
- `target` (string): Specific file or directory to analyze (default: `src/`)
- `strict` (boolean): Use strict mode for all tools (default: true)
- `fix` (boolean): Auto-fix formatting issues with black (default: false)

## Usage Examples

```bash
# Analyze entire codebase
Skill: code-analyzer

# Analyze specific module
Skill: code-analyzer --target src/todo/models.py

# Analyze and auto-fix formatting
Skill: code-analyzer --fix true

# Analyze with relaxed rules (not recommended)
Skill: code-analyzer --strict false
```

## Execution Steps

1. **Validate Environment**
   - Check black installed: `black --version`
   - Check flake8 installed: `flake8 --version`
   - Check mypy installed: `mypy --version`
   - If any missing, report error with installation command

2. **Run Black (Code Formatter)**
   ```bash
   black <target> --line-length 88 --check [--diff]
   ```
   - If `fix=true`: Remove `--check` to apply fixes
   - Track: Files that would be reformatted or were reformatted
   - Constitution requirement: Line length 88

3. **Run Flake8 (Linter)**
   ```bash
   flake8 <target> \
     --max-line-length=88 \
     --extend-ignore=E203,W503 \
     --max-complexity=10
   ```
   - Constitution requirements:
     - Ignore E203, W503 (black compatibility)
     - Max complexity: 10
   - Track: Total errors, errors by type, files with most errors

4. **Run Mypy (Type Checker)**
   ```bash
   mypy <target> --strict [--show-error-codes]
   ```
   - If `strict=false`: Use `--no-strict` instead
   - Constitution requirement: Strict mode
   - Track: Type errors by category, files with errors

5. **Analyze Code Complexity**
   - For each Python file in target:
     - Count lines of code (excluding comments/blanks)
     - Identify functions > 50 lines (constitution violation)
     - Identify files > 500 lines (constitution violation)
     - Calculate average function length
   - Use radon if available: `radon cc <target> -a`

6. **Generate Report**
   ```
   ==================== CODE ANALYZER REPORT ====================
   Target: <target>
   Timestamp: <ISO datetime>

   [BLACK - CODE FORMATTING]
   Status: <PASS/FAIL>
   Files checked: <count>
   Would reformat: <count> ❌
   [If fix=true:] Reformatted: <count> ✅

   [FLAKE8 - LINTING]
   Status: <PASS/FAIL>
   Total errors: <count>
   Files with errors: <count>
   Top issues:
   - <error_code>: <count> occurrences (<description>)
   [List up to 5 most common]

   [MYPY - TYPE CHECKING]
   Status: <PASS/FAIL>
   Files checked: <count>
   Type errors: <count>
   Top issues:
   - <file>:<line>: <error_summary>
   [List up to 5]

   [COMPLEXITY ANALYSIS]
   Status: <PASS/FAIL>
   Average function length: <lines>
   Constitutional violations:
   - Functions > 50 lines: <count>
     - <file>:<function> (<line_count> lines)
   - Files > 500 lines: <count>
     - <file> (<line_count> lines)

   [OVERALL QUALITY SCORE]
   Grade: <A/B/C/D/F>
   - A: All checks pass, no violations
   - B: Minor formatting issues only
   - C: Linting errors or few type errors
   - D: Multiple type errors or complexity violations
   - F: Significant issues across multiple categories

   [RECOMMENDATIONS]
   <Actionable steps to fix issues>
   =============================================================
   ```

7. **Exit Codes**
   - 0: All checks passed (Grade A)
   - 1: Formatting issues only (Grade B)
   - 2: Linting or type errors (Grade C-D)
   - 3: Critical violations (Grade F)

## Acceptance Criteria

- ✅ Runs all three quality tools: black, flake8, mypy
- ✅ Enforces constitutional standards (line length 88, complexity ≤10, strict typing)
- ✅ Identifies functions > 50 lines and files > 500 lines
- ✅ Provides prioritized list of issues (most common first)
- ✅ Generates quality grade (A-F) based on severity
- ✅ Offers actionable recommendations for fixes
- ✅ Supports auto-fix mode for black formatting
- ✅ Works on entire codebase or specific files

## Dependencies

- black
- flake8
- mypy
- radon (optional, for advanced complexity metrics)

## Error Handling

- **Tools not installed**: "Error: <tool> not found. Run: pip install black flake8 mypy"
- **Target not found**: "Error: Target '<target>' does not exist."
- **Invalid target type**: "Error: Target must be a .py file or directory containing Python files."

## Notes

- Run this skill before committing code (pre-commit hook candidate)
- Auto-fix (`--fix true`) is safe but review changes before committing
- Strict mypy mode catches errors early; disable only with justification
- Constitution compliance is NON-NEGOTIABLE; Grade C or below requires fixes
