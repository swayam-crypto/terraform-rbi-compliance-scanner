# ADR-001: Data-Driven Resource Definitions

**Status:** Accepted

**Date:** 2026-08-22

---

# Context

The platform is intended to support multiple cloud providers while minimizing provider-specific logic within the runtime.

Hardcoding cloud semantics into runtime components would make the platform difficult to maintain and extend.

---

# Decision

Cloud resource definitions will be maintained as catalog data rather than implemented directly in runtime code.

The catalog is responsible for describing cloud resources while the runtime consumes those definitions.

---

# Consequences

## Advantages

- Provider-independent runtime.
- Easier addition of new cloud providers.
- Reduced duplication.
- Resource behavior is driven by metadata.

## Trade-offs

- Greater dependence on catalog quality.
- Catalog validation becomes critical.

---

# Related Reviews

- Phase 02 – Canonical Architecture Review