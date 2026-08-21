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
## AD-007 - Runtime Model Ownership

**Status**

Open

**Priority**

High

**Review Phase**

Phase 02 – Canonical Architecture

**Description**

The platform currently contains two primary resource models:
    ResolvedResource
    CanonicalResource
The long-term ownership of the runtime model has not yet been formally defined.

**Impact**

Future runtime evolution, graph analysis, attack analysis, and rule execution depend on establishing a single authoritative runtime resource model.

**Proposed Resolution**

Document runtime ownership before implementing Runtime V2.

---

## AD-008 - Catalog API Coupling

**Status**

Open

**Priority**

Medium

**Review Phase**

Phase 02 – Canonical Architecture

**Description**

The catalog currently exposes APIs that operate directly on ResolvedResource.
If the platform adopts CanonicalResource as the runtime model, these interfaces may require architectural revision.

**Impact**

Future runtime migration may require catalog API changes.

**Proposed Resolution**

Review catalog interfaces during Runtime V2 planning.

---

## AD-009 – Parser Responsibility Growth

**Status:** Open

**Priority:** Medium

**Phase Identified:** Phase 05 – Parser Architecture Review

### Problem

The parser package has expanded beyond infrastructure parsing.

Current responsibilities include:

- Terraform parsing
- Terraform Plan parsing
- Expression resolution
- Provider resolution
- Resource normalization
- Caching
- Suppression handling

While these responsibilities are closely related today, continued platform growth may cause the parser package to become difficult to maintain.

### Impact

As additional Infrastructure-as-Code formats are supported, parser implementations may accumulate unrelated runtime responsibilities, increasing complexity and reducing maintainability.

### Recommendation

Maintain the current implementation.

Re-evaluate parser responsibilities when introducing additional infrastructure formats.

Potential future separations include:

- Expression evaluation
- Provider resolution
- Cache management
- Suppression processing

### Rationale

The current implementation remains appropriate for the existing platform.

This debt records a likely future architectural evolution rather than an immediate refactoring requirement.


# Completed

None.

---

# Deferred

None.

---

# Review History

| Phase | Status | Score | Debt Added | Summary |
|--------|--------|------:|------------|---------|
| Phase 01 – Runtime Architecture | Complete | 8.5 / 10 | AD-001 – AD-006 | Reviewed the runtime orchestration, execution flow, and shared runtime state. |
| Phase 02 – Canonical Architecture | Complete | 8.8 / 10 | AD-007 – AD-008 | Validated the canonical model and catalog architecture. |
| Phase 03 – Graph Runtime | Complete | 9.5 / 10 | None | Validated the graph runtime as the analytical foundation of the platform. |
| Phase 04 – Rule & Compliance Engine | Complete | 9.7 / 10 | None | Confirmed framework-neutral compliance architecture. |
| Phase 05 – Parser Architecture | Complete | 8.9 / 10 | AD-009 | Validated parser abstraction and documented parser responsibility growth. |
| Phase 06 – Testing Architecture | Complete | 9.6 / 10 | None | Validated the testing architecture, architectural contract testing, and regression strategy. |
| Phase 07 – Platform & Repository Architecture | Complete | 9.9 / 10 | None | Validated repository organization, documentation, packaging, CI/CD, release process, and engineering practices. |
| Phase 08 – Final Architecture Review | Pending | — | — | Not Started |
---

# Notes

This register is intentionally implementation-independent.

Architecture debt should only be marked as **Resolved** after the corresponding architectural milestone has been completed and merged into the main branch.

Architecture debt should never be deleted. Historical records provide valuable context for future architectural decisions.