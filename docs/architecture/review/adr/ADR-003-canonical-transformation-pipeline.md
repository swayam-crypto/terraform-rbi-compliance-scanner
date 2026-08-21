# ADR-003: Canonical Transformation Pipeline

**Status:** Accepted

**Date:** 2026-08-22

---

# Context

Canonical transformation should remain modular and maintainable.

---

# Decision

Transformation into the canonical model is implemented as a staged pipeline consisting of:

1. Classification
2. Attribute Mapping
3. Resource Construction

Each stage has a single responsibility.

---

# Consequences

## Advantages

- Easier testing.
- Easier extension.
- Clear separation of concerns.

---

# Related Reviews

- Phase 02 – Canonical Architecture Review