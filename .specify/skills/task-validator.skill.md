# Task Validator Agent Skill

## Purpose
Verify task completion against acceptance criteria defined in `specs/<feature>/tasks.md`. Ensures each task meets its requirements before marking as complete.

## Parameters

### Required
- `feature` (string): Feature name (e.g., "todo-core", "search-filter")
- `task_id` (string): Task ID to validate (e.g., "T1.1", "T2.3")

### Optional
- `auto_approve` (boolean): Auto-approve if all checks pass (default: false)
- `verbose` (boolean): Show detailed validation steps (default: true)

## Usage Examples

```bash
# Validate specific task
Skill: task-validator --feature todo-core --task_id T1.1

# Validate with auto-approval
Skill: task-validator --feature search-filter --task_id T3.2 --auto_approve true

# Quiet mode (only show result)
Skill: task-validator --feature todo-core --task_id T2.1 --verbose false
```

## Execution Steps

1. **Load Task Definition**
   - Read `specs/<feature>/tasks.md`
   - Find task with ID `<task_id>`
   - Parse:
     - Task description
     - Acceptance criteria (checklist items)
     - Expected files/modules
     - Test requirements
   - If task not found: Error and exit

2. **Validate File Existence**
   - Check that all files mentioned in task description exist
   - Verify files are in expected locations (src/, tests/)
   - Report missing files as validation failures

3. **Validate Tests**
   - If task requires tests:
     - Find corresponding test file (e.g., `tests/test_<module>.py`)
     - Verify test file exists
     - Search for test functions related to task (by naming convention)
     - Run tests: `pytest <test_file> -v`
     - Check all related tests pass
   - If no tests required: Skip this step

4. **Check Code Quality**
   - Run code-analyzer skill on files modified/created by this task
   - Verify Grade A or B (no critical issues)
   - Check constitutional compliance:
     - Functions ≤ 50 lines
     - Files ≤ 500 lines
     - Type hints present
     - Docstrings for public APIs

5. **Validate Acceptance Criteria**
   - For each acceptance criterion in tasks.md:
     - Display criterion
     - Prompt: "Is this criterion met? (y/n/skip)"
     - If `auto_approve=true`: Check programmatically if possible
   - Examples of programmatic checks:
     - "Function X exists" → grep/search for function definition
     - "Tests pass" → Already validated in step 3
     - "Type hints present" → mypy passes
   - Manual verification for subjective criteria (UX, error messages)

6. **Generate Validation Report**
   ```
   ==================== TASK VALIDATION REPORT ====================
   Feature: <feature>
   Task ID: <task_id>
   Description: <task_description>
   Timestamp: <ISO datetime>

   [FILE VALIDATION]
   Expected files: <count>
   ✅ Found: <file_list>
   ❌ Missing: <file_list>

   [TEST VALIDATION]
   Test file: <test_file>
   Tests run: <count>
   ✅ Passed: <count>
   ❌ Failed: <count>
   [If failures:] Failed tests: <test_names>

   [CODE QUALITY]
   Quality grade: <A/B/C/D/F>
   Issues: <count>
   [If issues:] Top issues: <issue_summary>

   [ACCEPTANCE CRITERIA]
   Total criteria: <count>
   ✅ Met: <count>
   ❌ Not met: <count>
   ⚠️  Skipped: <count>

   Criteria details:
   ✅ <criterion 1>
   ✅ <criterion 2>
   ❌ <criterion 3> (Reason: <explanation>)
   ⚠️  <criterion 4> (Skipped)

   [OVERALL RESULT]
   Status: <PASS/FAIL/INCOMPLETE>
   - PASS: All checks passed, task ready to mark complete
   - FAIL: Critical failures (tests failed, files missing, quality grade D/F)
   - INCOMPLETE: Some criteria not met or skipped

   [RECOMMENDATIONS]
   <Actionable next steps if FAIL or INCOMPLETE>
   ===============================================================
   ```

7. **Update Task Status (Optional)**
   - If `auto_approve=true` AND status=PASS:
     - Update tasks.md to mark task as complete (add ✅ or checkmark)
     - Commit change: `git add specs/<feature>/tasks.md && git commit -m "chore: mark task <task_id> complete"`

8. **Exit Codes**
   - 0: PASS (all criteria met)
   - 1: FAIL (critical failures)
   - 2: INCOMPLETE (some criteria not met)

## Acceptance Criteria

- ✅ Loads task definition from tasks.md correctly
- ✅ Validates all expected files exist
- ✅ Runs and validates tests if required
- ✅ Checks code quality using code-analyzer skill
- ✅ Validates each acceptance criterion (programmatically where possible)
- ✅ Provides clear PASS/FAIL/INCOMPLETE status
- ✅ Offers actionable recommendations for failures
- ✅ Optionally auto-approves and updates tasks.md

## Dependencies

- code-analyzer skill
- pytest (for test validation)
- git (for auto-approval commits)

## Error Handling

- **Feature not found**: "Error: Feature '<feature>' not found. Check specs/<feature>/tasks.md exists."
- **Task ID not found**: "Error: Task '<task_id>' not found in tasks.md."
- **Invalid task format**: "Error: Task '<task_id>' missing acceptance criteria."
- **No permission to update**: "Warning: Cannot auto-approve. No write permission to tasks.md."

## Notes

- Use this skill in the "Green" phase of TDD (after tests pass)
- Integrates with `/validate-tier` command for tier completion validation
- Manual verification still required for subjective criteria (UX, readability)
- Auto-approval useful for CI/CD pipelines but review commits carefully
