# ADR-004: Immutable Domain Models

**Status:** Accepted

**Date:** 2026-08-22

---

# Context

Core runtime objects should remain predictable during analysis.

---

# Decision

Core domain models will be immutable wherever practical.

Examples include:

- CanonicalResource
- Catalog definitions

---

# Consequences

## Advantages

- Prevents accidental mutation.
- Easier reasoning.
- Safer concurrent analysis.

---

# Related Reviews

- Phase 02 – Canonical Architecture Review