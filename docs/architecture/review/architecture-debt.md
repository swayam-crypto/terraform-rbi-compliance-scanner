# Architecture Debt Register

This document tracks architectural debt identified during the architecture review.

Architectural debt differs from implementation bugs or feature requests. It represents design decisions, incomplete abstractions, or structural limitations that may affect the long-term evolution of the platform.

Each debt item includes:

- A unique identifier
- Current status
- Priority
- Review phase
- Description
- Impact
- Proposed resolution

---

# Priority Levels

## High

Architectural issues that directly affect platform evolution or future major features.

## Medium

Architectural improvements that should be completed before the first stable platform release.

## Low

Maintainability improvements that do not currently limit development.

---

# High Priority

---

## AD-001 — Canonical Runtime

**Status**

Open

**Priority**

High

**Review Phase**

Phase 01 – Runtime Architecture

**Description**

The runtime currently operates on `ResolvedResource` while the canonical cloud model exists as a separate architecture.

The graph engine, attack engine, runtime, and rule engine all operate on `ResolvedResource`, preventing `CanonicalResource` from becoming the platform's primary runtime abstraction.

**Impact**

This limits provider-independent infrastructure analysis and delays the transition toward a fully canonical runtime.

**Proposed Resolution**

Implement Runtime V2 by migrating runtime components to operate on `CanonicalResource`.

---

## AD-002 — Runtime Analysis Abstraction

**Status**

Open

**Priority**

High

**Review Phase**

Phase 01 – Runtime Architecture

**Description**

Runtime analyses are exposed individually through `ScanContext` (currently `attack_paths`).

As additional analyses are introduced (blast radius, identity, privilege, risk, etc.), ScanContext risks becoming a collection of unrelated analysis objects.

**Impact**

Future analysis engines may become tightly coupled to ScanContext and increase runtime complexity.

**Proposed Resolution**

Introduce a generalized analysis abstraction that becomes the single entry point for runtime analysis results.

---

# Medium Priority

---

## AD-003 — Runtime Orchestration

**Status**

Open

**Priority**

Medium

**Review Phase**

Phase 01 – Runtime Architecture

**Description**

Runtime orchestration is centralized within `scan_resources()`.

Each new analysis stage currently requires modifications to the runtime execution pipeline.

**Impact**

Runtime complexity will continue increasing as new analysis engines are introduced.

**Proposed Resolution**

Introduce a dedicated runtime orchestration layer after the analysis architecture has been finalized.

---

## AD-004 — Graph Rule Architecture

**Status**

Open

**Priority**

Medium

**Review Phase**

Phase 01 – Runtime Architecture

**Description**

Graph rule implementations currently perform graph reasoning directly rather than consuming precomputed runtime analysis.

Additionally, production and experimental graph-rule implementations currently coexist.

**Impact**

Graph reasoning is duplicated and the graph-rule subsystem remains incomplete.

**Proposed Resolution**

Complete the graph-rule architecture and migrate graph rules to consume runtime analysis.

---

# Low Priority

---

## AD-005 — Parser Modernization

**Status**

Open

**Priority**

Low

**Review Phase**

Phase 01 – Runtime Architecture

**Description**

The parser currently contains both legacy procedural APIs and the newer InfrastructureParser abstraction.

**Impact**

The coexistence of two parser styles increases maintenance complexity but does not currently affect runtime correctness.

**Proposed Resolution**

Gradually consolidate parser functionality around the InfrastructureParser abstraction and retire legacy entry points.

---

## AD-006 — Duplicate GraphRule Base

**Status**

Open

**Priority**

Low

**Review Phase**

Phase 01 – Runtime Architecture

**Description**

Two GraphRule base implementations currently exist in separate packages.

**Impact**

This creates unnecessary duplication and increases maintenance effort.

**Proposed Resolution**

Unify graph-rule inheritance under a single shared GraphRule abstraction.

---

# Completed

None.

---

# Deferred

None.

---

# Review History

| Phase | Debt Items |
|--------|------------|
| Phase 01 – Runtime Architecture | AD-001, AD-002, AD-003, AD-004, AD-005, AD-006 |

---

# Notes

This register is intentionally implementation-independent.

Architecture debt should only be marked as **Resolved** after the corresponding architectural milestone has been completed and merged into the main branch.

Architecture debt should never be deleted. Historical records provide valuable context for future architectural decisions.