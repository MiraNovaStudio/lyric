# Adhoc math module test -- 20260228.1044

## Summary
Created `lyric/tests/python_modules/core_math.ly` -- a comprehensive Lyric program that exercises
every public function and constant in Python's `math` module via `importpy math`. All 150+ tests
pass (100% PASS output). Also discovered and documented that non-ASCII characters (e.g. Unicode
`U+2248 ≈`) in string literals cause a UnicodeEncodeError on Windows/Git Bash stdout; labels must
use ASCII-only characters.

## Files Changed
- `lyric/tests/python_modules/core_math.ly` -- New: adhoc test covering all math module features:
    constants (pi, e, tau, inf, nan), rounding (ceil/floor/trunc), fabs, factorial, gcd/lcm,
    isqrt, comb/perm, isfinite/isinf/isnan, sqrt, pow, exp/expm1, log/log2/log10/log1p,
    degrees/radians, sin/cos/tan/asin/acos/atan/atan2, hypot, sinh/cosh/tanh/asinh/acosh/atanh,
    copysign, fmod, remainder, ldexp, modf, frexp, fsum, prod, erf/erfc, gamma/lgamma.

## Reason
Adhoc integration test to verify that `importpy math` works end-to-end in Lyric and that the
interpreter fixes from the previous session (try-scope isolation, Python instance method dispatch)
enable correct math function calls, variable argument passing, and multi-arg function calls.

## Git Commit Hash
`TBD` - Adhoc math module test

## Status
✅ Completed
