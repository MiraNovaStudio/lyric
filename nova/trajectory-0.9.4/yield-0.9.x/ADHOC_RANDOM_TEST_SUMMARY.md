# Adhoc random Module Test Summary

## Task
Add `random` to the `importpy` whitelist and create `lyric/tests/python_modules/core_random.ly`
to exercise every public function of Python's `random` module through Lyric's `importpy` system.

## Key Accomplishments
- Added `'random'` to `WHITELISTED_MODULES` in `lyric/pyproxy.py`
- Created `core_random.ly` with 100% PASS across all tests
- Sections covered:
    - Seeding and reproducibility: seed, getstate, setstate
    - Basic random: random()
    - Bounded random: uniform(), randint(), randrange()
    - Sequence operations: choice(), choices(), shuffle()
    - Sampling: sample()
    - Distributions: gauss, normalvariate, expovariate, betavariate, gammavariate,
      lognormvariate, vonmisesvariate, paretovariate, weibullvariate, triangular
    - Bit-level: getrandbits(), randbytes()
- Updated `test_importpy_whitelist.py` to reflect random's new whitelisted status
- All 1114 pytest tests pass (1112 + 2 new random whitelist tests)

## Discovery: ArrObject is not a collections.abc.Sequence
Python 3.11+ `random.sample` requires `isinstance(population, Sequence)`. Lyric's `ArrObject`
has `__len__`, `__getitem__`, `__setitem__`, `__iter__` but is NOT registered with
`collections.abc.Sequence`, so it fails the isinstance check. Workaround: use `pool.elements`
to access the underlying Python list of an ArrObject.

## Discovery: random.choices k is keyword-only
`random.choices(population, weights=None, *, cum_weights=None, k=1)` — `k` is keyword-only.
Passing it positionally assigns the value to `weights`. Solution: call without k argument to
use the default (k=1).

## Files Created/Modified
- `lyric/pyproxy.py` — Added `'random'` to `WHITELISTED_MODULES`
- `lyric/tests/python_modules/core_random.ly` — New adhoc test (100% PASS)
- `lyric/tests/core-0.9.0/test_importpy_whitelist.py` — Updated 2 tests, added 2 new tests

## Test Results
- `lyric run lyric/tests/python_modules/core_random.ly` -- 100% PASS
- `pytest lyric/tests/ -q` -- 1114 passed, 0 failed

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260228/1054-CHANGELOG.md`
