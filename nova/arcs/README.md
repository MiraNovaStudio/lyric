# MiraNova Arc System

## Overview

The **Arc System** defines the long-term organizational structure for all MiraNova and Lyric development.  
It was **conceived and designed by Michael “Aeonath” Emch**, who established the terminology and hierarchy of **Arc → Trajectory → Yield** to describe the studio’s iterative release process.

This framework blends *Agile discipline* with *MiraNova’s creative identity*, ensuring each stage of progress is both traceable and thematically coherent.

---

## 🔷 Hierarchical Model

### 1. **Arc**
**Path:** `/nova/arcs/`

An **Arc** represents a broad era of development — a continuous record of all major trajectories in Lyric’s evolution.  
Each Arc contains multiple **Trajectories**, each targeting a significant milestone or release goal.

Example:
```
/nova/arcs/
trajectory-0.9.1/
trajectory-1.0.0/
trajectory-2.0.0/
```


---

### 2. **Trajectory**
**Path:** `/nova/arcs/trajectory-x.x.x/`

A **Trajectory** is a focused path of development aimed at a specific *major* or *intermediate* release version.  
Each trajectory begins where the previous one concluded.

Example:

```
/nova/arcs/trajectory-0.9.1/
yield-0.1.0/
yield-0.2.0/
yield-0.3.0/
yield-0.3.4/
yield-0.9.1/
```


---

### 3. **Yield**
**Path:** `/nova/arcs/trajectory-x.x.x/yield-x.x.x/`

A **Yield** represents a single iteration of focused work — what would traditionally be called a *sprint*.  
Each Yield directory contains the planning, execution, and completion artifacts that produced a specific version of the system.

Example:

```
/nova/arcs/trajectory-0.9.1/yield-0.3.0/
SPRINT3_PLAN.md
SPRINT3_TASK1_SUMMARY.md
SPRINT3_DOD_SUMMARY.md
SPRINT3_CODE_REVIEW.md
```


---

## 🧭 Versioning Philosophy

| Prefix | Example | Meaning |
|---------|----------|---------|
| `dev-` | `dev-0.3.0` | Internal milestone tags during development |
| `alpha-` | `alpha-0.9.1` | Public early preview (feature-complete but unstable) |
| `beta-` | `beta-0.9.5` | Wider testing before a major version |
| `rel-` | `rel-1.0.0` | Stable public release milestone |
| `fix-` | `fix-1.0.1` | Minor hotfix or patch release |

Each Yield corresponds to one of these tag states in Git.  
Collectively, the Yields within a Trajectory lead up to that Trajectory’s final milestone tag.

---

## 🌌 Example: Active Arc Layout
```
/nova
/arcs
README.md
/trajectory-0.9.1
yield-0.1.0/ → early syntax prototype
yield-0.2.0/ → interpreter foundation
yield-0.3.0/ → type system integration
yield-0.3.4/ → lazy proxy & reflection
yield-0.9.1/ → public alpha build
alpha-0.9.1 tag
/trajectory-1.0.0
yield-0.9.5/ → pre-beta polish
yield-0.9.9/ → beta testing & stability
yield-1.0.0/ → first stable release
rel-1.0.0 tag
```


---

## 🌱 Terminology Summary

| Term | Meaning |
|------|----------|
| **Arc** | The full lineage of Lyric’s evolution — all trajectories combined |
| **Trajectory** | A development cycle leading toward a major or intermediate release |
| **Yield** | A discrete iteration (formerly “sprint”) that produces a new version |
| **Version Tag** | The Git label marking a yield or release milestone |
| **DoD** | Definition of Done document marking yield completion |
| **Plan** | The blueprint for work performed during that yield |

---

## ✨ Design Philosophy

The Arc System ensures that every step in Lyric’s evolution is transparent, traceable, and meaningful —  
from internal dev builds to public releases — forming a complete living history of MiraNova’s development journey.

---

**Author:** Michael “Aeonath” Emch  
**Architectural Documentation:** ChatGPT  
**Engineering Implementation:** Claude  
**Last Updated:** October 2025

