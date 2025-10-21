# Lyric Module System Design Overview

**Prepared by:** Aeonath  
**Revision:** 1.0  
**Date:** October 20, 2025  
**Project:** Lyric (dev-core)  
**Purpose:** Define the architecture and design plan for Lyric’s module import system, including native modules and Python interoperability.

---

## 🧭 Overview

Lyric will support two complementary module types:

1. **Native Lyric Modules** — written directly in Lyric and loaded by the interpreter.  
2. **Python Bridge Modules (`importpy`)** — fallback access to Python libraries for interoperability.

This hybrid design allows Lyric to remain self-contained while leveraging Python’s vast ecosystem when necessary.

---

## 🧩 Native Lyric Modules

### Description
Modules written entirely in Lyric (`.ly` or future `.lym` format) that are directly interpreted and cached by Lyric’s runtime.

### Goals
- Full compatibility with Lyric’s type system and runtime.  
- Portable and self-contained (no Python dependency).  
- Fast load times and consistent behavior across environments.  

### Import Syntax

```
import mathutils
import io
import string
```


### Advantages
- No cross-runtime translation or wrapping overhead.  
- Predictable performance.  
- Safe for future standalone Lyric builds.  

### Implementation Notes
- Implement a `ModuleLoader` class to resolve and cache Lyric modules.  
- Maintain a module search path similar to Python’s `sys.path`.  
- Support a small standard library (math, io, string, json, system).

---

## 🧠 Python Bridge Modules (`importpy`)

### Description
Optional interoperability layer that allows importing standard Python packages (e.g., `numpy`, `requests`) for advanced functionality or experimentation.

### Import Syntax

```
importpy numpy
importpy requests
```


### Behavior
- Uses Python’s `importlib` to load the target module.  
- Injects a wrapped version of the module into the Lyric runtime.  
- Converts Lyric objects to Python primitives before invocation.  
- Wraps Python return values back into Lyric types.  

### Caveats
- Performance will be significantly slower due to type conversion.  
- Type mismatches may occur if Python functions expect native primitives.  
- Python exceptions will need translation to Lyric runtime errors.  
- Not secure for sandboxed environments without restrictions.  

### Use Cases
- Accessing mature scientific libraries (NumPy, Requests).  
- Rapid prototyping or experimental integrations.  
- Temporary fallback until a Lyric-native standard library matures.

---

## ⚙️ Import Resolution Order

1. **Native Lyric module** — found in the Lyric search path.  
2. **Built-in Lyric standard library module** — included with runtime.  
3. **Python bridge module** — imported via `importpy`.  
4. **Failure** — raises a Lyric `ModuleNotFoundError`.

---

## 🔬 Implementation Roadmap

| Version | Goal | Description |
|----------|------|-------------|
| **0.5.0** | Runtime Stabilization | Finalize type enforcement and interpreter stability. |
| **0.6.0** | Python Bridge Layer | Implement `importpy` keyword and basic module wrapping. |
| **0.7.0** | Native Module Loader | Add Lyric `ModuleLoader` and module caching system. |
| **0.8.0** | Lyric Standard Library | Implement first native modules (`math`, `io`, `string`). |
| **1.0.0** | Hybrid Interoperability | Stable dual import system with performance optimizations. |

---

## 🧩 Key Design Principles

1. **Clarity Over Complexity**  
   Explicit separation between native and Python imports avoids confusion.  
2. **Performance Transparency**  
   Users know when they are crossing into Python (importpy).  
3. **Long-Term Independence**  
   Lyric modules will eventually replace most Python dependencies.  
4. **Extensibility**  
   The module loader should support packaging, caching, and compiled modules later.

---

## 🚀 Example Future Usage

```
import mathutils
importpy numpy

var arr = numpy.array([1, 2, 3])
print(arr.sum())

var angle = mathutils.sin(90)
print(angle)
```