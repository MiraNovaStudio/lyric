# Lyric Testing Structure

## Overview
Lyric’s unit testing framework is organized **per sprint**, mirroring the project’s iterative development cycle.  
Each sprint introduces new functionality or refactors existing components, and its test suite serves as the validation layer for that sprint’s deliverables.

This model aligns with the MiraNova Rapid Sprint philosophy:
> Every sprint builds upon a validated foundation.  
> All prior sprints’ tests must continue to pass before a new sprint is considered complete.

---

## Directory Layout


```
tests/
├─ core-0.1.0/
├─ core-0.2.0/
├─ core-0.3.0/
└─ core-0.4.0/
```


### Folder Descriptions
- **core-0.x.x/**  
  Each folder represents the complete test suite for a given sprint version.  
  Tests validate all new or modified functionality introduced during that sprint.

Older sprint folders remain permanently in the repository as historical validation checkpoints.

---

## Testing Philosophy
All tests across all sprints are executed together to ensure full regression stability.  
Prior sprints are implicitly shared — if an earlier feature breaks, its original tests will detect the regression.

There is no need for a `shared/` directory or global fixture set;  
the cumulative collection of sprint folders *is* the shared validation baseline.

---

## Running Tests

Run all tests (recommended):
```bash
pytest tests/
```

Run tests for a specific sprint:

```
pytest tests/core-0.3.0
```


Run a specific module:


```
pytest tests/core-0.3.0/test_types.py
```

