# Claude Configuration — Lyric Project (dev-core)

## 🚨 CRITICAL WORKFLOW RULE 🚨
**NEVER COMMIT ANY CHANGES WITHOUT CREATING A CHANGELOG ENTRY FIRST!**
This applies to ALL filesystem modifications - code, config, docs, renames, deletions, etc.

## 🖥️ SHELL ENVIRONMENT REMINDER 🖥️
**YOU ARE RUNNING POWERSHELL, NOT BASH!**
- Use PowerShell commands: `Get-Date -Format "yyyyMMdd/HHmm"` NOT `date +"%Y%m%d/%H%M"`
- Use PowerShell syntax for all terminal operations
- Remember: Windows PowerShell environment in Cursor

## User Control Configuration

### Git Commit Toggle

Should I commit changes to git and write changelog?
USER_RESPONSE: YES


**Options**
- **YES** – Claude will document, stage, commit, and write changelog entries.
- **NO** – Skip changelog and git operations; useful during debugging.

### Deployment Toggle (Lyric Is Interpreted)

Should I deploy the project after changes?
USER_RESPONSE: NO


**Notes**
- Lyric is an interpreted language; it does not require compilation or S3 deployment.
- Deployment toggles exist only for future use if Nova adds publishing features.
- Setting `NO` means all work remains local and version-controlled only.

---

## Standard Development Process

### 1. Preparation
- Ensure `dev-core` branch is checked out.
- Verify `.gitignore` excludes build artifacts (`__pycache__`, `.egg-info`, etc.).
- Confirm both toggles in this config are correct before each iteration.

### 2. Modify or Generate Code
Claude will:
- Create or update files inside `/lyric/`, `/tests/`, and `/examples/`.
- Maintain imports and Python package integrity.
- Ensure new modules import cleanly.

### 3. Write Summary (Conditional)
If **Git Commit Toggle = YES**, Claude writes a changelog entry:

**MANDATORY REQUIREMENT**: Always get the current date and time before creating changelog files.

**Changelog Path Format:**
nova/changelog/YYYYMMDD/TIME_HHMM-CHANGELOG.md

**Time Format**: Use 24-hour format (e.g., 1430 for 2:30 PM, 0915 for 9:15 AM)

**Include**
- Commit hash
- Files changed
- Summary of implementation
- Status (✅ done / ⏳ pending)
- Relevant sprint and task references

### 4. Write Sprint Task Summary (Conditional)
If **Git Commit Toggle = YES**, Claude writes a sprint task summary:


nova/sprints/sprintX/SPRINTX_TASKX_SUMMARY.md


**Naming Convention**: Always use SPRINTX_TASKX_SUMMARY.md format (e.g., SPRINT1_TASK1_SUMMARY.md, SPRINT1_TASK2_SUMMARY.md)

**Include**
- Brief task completion summary
- Key accomplishments
- Files created/modified
- Status (✅ Completed)
- Reference to changelog for details

### 5. Write Sprint DOD Summary (Conditional)
If **Git Commit Toggle = YES** and sprint is complete, Claude writes a sprint definition of done summary:


nova/sprints/sprintX/SPRINTX_DOD_SUMMARY.md


**Include**
- Sprint objective summary
- All tasks completed status
- Definition of done criteria verification
- Overall sprint status (✅ Completed)
- Reference to all task summaries and changelogs

### 6. Git Add & Commit (Conditional)

**🚨 CRITICAL REQUIREMENT 🚨**: 
**NEVER COMMIT WITHOUT CREATING A CHANGELOG ENTRY FIRST!**

**This applies to ALL commits, including:**
- File modifications
- File deletions  
- File renames/moves
- Directory changes
- Configuration updates
- Documentation changes
- ANY filesystem modification

**Final Step Process:**
1. **REQUIRED**: Create changelog entry (Step 3) - **MUST BE DONE FIRST**
2. **REQUIRED**: Create sprint task summary (Step 4) 
3. **REQUIRED**: Create sprint DOD summary (Step 5) if sprint complete
4. Stage all new files: `git add *`
5. Commit all changes: `git commit -a -m "SprintX TaskY: <brief description>"`

```bash
git add *
git commit -a -m "SprintX TaskY: <brief description>"
```

**Commit Message Format**: 
- **MUST** be one line only
- **MUST** include sprint number and task number
- **MUST** be concise (e.g., "Sprint1 Task2: Implement Lexer", "Sprint1 Task4: Implement Parser")
- **MUST NOT** include detailed descriptions (those go in changelog entries)

**Note**: This process ensures that:
- Changelog entries are ALWAYS created before commits
- New files created (changelog entries, task summaries, DOD summaries) are staged with `git add *`
- All modifications to existing files are included with `git commit -a`
- Both new documentation and code changes are committed together
- Commit messages are concise and follow the SprintX TaskY format

Keep commit messages short; details live in changelog entries.

### Changelog Format

# SprintX TaskY — YYYYMMDD.HHMM

## Summary
Short explanation of what was implemented or fixed.

## Files Changed
- lyric/lexer.py — implemented tokenizer
- tests/test_lexer.py — added baseline tests

## Reason
Establishes foundational lexer and test coverage for Lyric v0.1

## Git Commit Hash
`abc1234` - Sprint1 Task2 Implementation

## Status
✅ Completed


## Safety & Validation Rules

Claude must never delete directories without confirmation.

Always include commit hash in changelog.

All generated Python files must be syntactically valid and importable.

Unit tests must run via pytest -q without fatal errors.

CLI command lyric run examples/hello.ly must work after Sprint 1 completion.

## Summary

No build/deploy steps.

Focus: Pure interpreted language development.

Goal: Maintain structured commits, organized changelogs, and validated tests.
