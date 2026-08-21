# ADR-002: Catalog Owns Cloud Semantics

**Status:** Accepted

**Date:** 2026-08-22

---

# Context

Cloud-specific knowledge should exist in a single location.

Duplicating cloud semantics across parsers, runtime components, and rules increases maintenance complexity.

---

# Decision

The catalog is the authoritative source for cloud semantics.

The catalog defines:

- Canonical types
- Resource kinds
- Capabilities
- Attributes
- Relationships
- Aliases
- Metadata

Runtime components consume catalog definitions.

---

# Consequences

## Advantages

- Single source of truth.
- Easier maintenance.
- Better multi-cloud support.

## Trade-offs

- Catalog schema becomes foundational.

---

# Related Reviews

- Phase 02 – Canonical Architecture Review