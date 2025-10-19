# Claude Configuration — Lyric Project (dev-core)

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


nova/changelog/YYYYMMDD/TIME_HHMM-CHANGELOG.md


**Include**
- Commit hash
- Files changed
- Summary of implementation
- Status (✅ done / ⏳ pending)
- Relevant sprint and task references

### 4. Git Add & Commit (Conditional)

```bash
git add -A
git commit -m "SprintX: <short message>"
```

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
