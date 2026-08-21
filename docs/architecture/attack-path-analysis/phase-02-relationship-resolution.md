# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---
# Phase 2 - Relationship Model Audit

---

## File

canonical/relationship_resolver.py

### Responsibility

Discovers infrastructure relationships from provider resources.

Converts provider-specific references into provider-independent graph edges.

Produces the Relationship objects that populate the RelationshipGraph.

### Current Capabilities

- Uses catalog relationship definitions.
- Resolves Terraform resource references.
- Validates target resource existence.
- Validates canonical target type.
- Produces directed relationships.
- Provider-independent implementation.

### Strengths

Excellent separation of responsibilities.

Relationship discovery is isolated from graph construction.

No traversal logic.

No compliance logic.

No attack logic.

Relationship extraction is entirely driven by the Resource Catalog.

This makes adding Azure, GCP or Kubernetes relationship extraction possible without changing the graph runtime.

### Weaknesses

Current implementation resolves only explicit infrastructure references.

Examples:

- subnet_id
- security_group_ids
- route_table_id

It does not infer relationships.

Future examples might include:

- implicit network reachability
- trust relationships
- IAM privilege relationships
- routing behavior
- internet accessibility

These are intentionally outside the current scope.

### Attack Path Impact

RelationshipResolver should remain responsible only for discovering relationships.

Attack path analysis must consume the graph produced by RelationshipResolver.

It must never infer or create additional infrastructure relationships.

### Decision

No architectural changes required.

RelationshipResolver is approved as the graph construction stage.

---

## File

graph/relationship.py

### Responsibility

Represents a directed edge between two infrastructure resources.

Acts as the canonical graph edge model.

### Current Structure

- source
- target
- relationship_type
- metadata

### Strengths

Simple.

Immutable.

Provider-independent.

Future-proof because metadata already exists.

### Weaknesses

Relationship metadata is currently unused.

Potential future metadata could include:

- inferred
- confidence
- provider
- protocol
- port
- trust_level
- exposure
- traversal_cost

None are required for Attack Path Analysis v1.

### Attack Path Impact

The current Relationship model is sufficient.

Attack path analysis should treat relationships as immutable graph edges.

No modifications are required before implementing attack path analysis.

### Decision

Relationship model is approved.

No changes required.

---

# Phase 2 Decision

Relationship resolution is complete.

The graph produced by the canonical pipeline is suitable for attack path analysis.

Attack path analysis should operate entirely as a consumer of the graph rather than extending or modifying relationship resolution.
