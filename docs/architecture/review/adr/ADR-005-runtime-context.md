# ADR-005: Runtime Context

**Status:** Accepted

**Date:** 2026-08-22

---

# Context

Multiple runtime components require shared access to analysis state.

Passing many independent objects increases coupling.

---

# Decision

Runtime state will be shared through a single ScanContext object.

The context contains shared runtime information required during scanning.

---

# Consequences

## Advantages

- Cleaner APIs.
- Centralized runtime state.
- Easier future extension.

---

# Related Reviews

- Phase 01 – Runtime Architecture Review