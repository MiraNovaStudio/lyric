# Adhoc random module whitelist + test -- 20260228.1054

## Summary
Added `random` to the `importpy` whitelist in `pyproxy.py` and created a comprehensive adhoc
Lyric test `core_random.ly` covering all functions of Python's `random` module. Updated two
existing whitelist tests that used `random` as the non-whitelisted example module.

## Files Changed
- `lyric/pyproxy.py` — Added `'random'` to `WHITELISTED_MODULES` frozenset
- `lyric/tests/python_modules/core_random.ly` — New: adhoc test covering all random module
  features: seed/state, random(), uniform(), randint(), randrange(), choice(), choices(),
  shuffle(), sample(), all distributions (gauss, normalvariate, expovariate, betavariate,
  gammavariate, lognormvariate, vonmisesvariate, paretovariate, weibullvariate, triangular),
  getrandbits(), randbytes()
- `lyric/tests/core-0.9.0/test_importpy_whitelist.py` — Updated two tests:
  - `test_importpy_random_blocked_without_unsafe` renamed to `test_importpy_itertools_blocked_without_unsafe`
    and updated to use `itertools` (now non-whitelisted) as the example blocked module
  - `test_unsafe_mode_off_by_default` updated to use `importpy json` instead of `importpy random`
  - Added `test_whitelist_contains_random` to verify random membership in whitelist
  - Added `test_importpy_random_whitelisted` to verify random imports without --unsafe

## Reason
`random` is a safe, commonly used standard library module with no interpreter internals access.
Adding it to the whitelist enables random number generation in Lyric programs without requiring
the --unsafe flag. Two workarounds required: (1) `choices` k parameter is keyword-only, called
without k argument; (2) `sample` requires `isinstance(population, Sequence)` — ArrObject does
not satisfy this, so `pool.elements` (inner Python list) is passed instead.

## Git Commit Hash
`TBD` - Adhoc random module whitelist + core_random.ly test

## Status
✅ Completed
