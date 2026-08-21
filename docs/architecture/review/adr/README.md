# Architecture Decision Records (ADR)

This directory contains the Architecture Decision Records (ADRs) for the Cloud Compliance Intelligence Platform.

An ADR documents a significant architectural decision, the context in which it was made, and its consequences.

Unlike architecture reviews, ADRs describe deliberate design decisions rather than evaluations or observations.

---

# Purpose

The goals of Architecture Decision Records are to:

- Record important architectural decisions.
- Document the reasoning behind those decisions.
- Preserve architectural history.
- Provide future contributors with context.
- Prevent previously resolved decisions from being repeatedly revisited.

---

# Relationship to Architecture Reviews

The project separates architecture reviews from architecture decisions.

## Architecture Reviews

Location:

```
docs/architecture/review/
```

Purpose:

- Evaluate the current architecture.
- Identify strengths and weaknesses.
- Record architectural debt.
- Recommend future improvements.

Reviews answer:

> What does the architecture look like today?

---

## Architecture Decision Records

Location:

```
docs/architecture/adr/
```

Purpose:

- Document accepted architectural decisions.
- Record proposed architectural changes.
- Explain why decisions were made.

ADRs answer:

> Why was this architectural decision made?

---

# ADR Lifecycle

Each Architecture Decision Record has a status.

## Proposed

A decision under discussion.

The architecture review has identified the need for a decision, but implementation has not begun.

---

## Accepted

The decision has been approved and represents the intended platform architecture.

---

## Superseded

The decision has been replaced by a newer ADR.

Older ADRs remain for historical reference.

---

## Deprecated

The decision is no longer recommended for future development but remains part of the project's architectural history.

---

# ADR Format

Each ADR follows the same structure.

- Title
- Status
- Date
- Context
- Decision
- Consequences
- Related Reviews

---

# Numbering

ADRs are numbered sequentially.

Examples:

```
ADR-001
ADR-002
ADR-003
```

Numbers are never reused.

If an ADR becomes obsolete, its status changes rather than deleting the document.

---

# Modification Policy

Architecture Decision Records are historical documents.

They should not be rewritten after acceptance.

If the architecture changes, create a new ADR referencing the previous decision.

Example:

```
ADR-007
↓

Superseded by

↓

ADR-012
```

This preserves the complete architectural history of the platform.

---

# Current ADRs

| ADR | Status | Description |
|-----|--------|-------------|
| ADR-001 | Accepted | Data-Driven Resource Definitions |
| ADR-002 | Accepted | Catalog Owns Cloud Semantics |
| ADR-003 | Accepted | Canonical Transformation Pipeline |
| ADR-004 | Accepted | Immutable Domain Models |
| ADR-005 | Accepted | Runtime Context |
| ADR-006 | Accepted | Graph-Based Runtime |
| ADR-007 | Proposed | Runtime Ownership |
| ADR-008 | Proposed | Runtime Analysis Abstraction |

---

# Guiding Principle

Architecture should evolve intentionally.

Every significant architectural decision should be documented before implementation whenever practical.

The combination of Architecture Reviews and Architecture Decision Records provides both:

- an understanding of the current architecture, and
- a documented history of how the architecture evolved over time.