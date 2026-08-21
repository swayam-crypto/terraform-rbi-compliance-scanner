# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---

# Phase 1 - Graph Foundation Audit

---

## File

graph/relationship_graph.py

### Responsibility

Stores the directed infrastructure relationship graph.

Provides efficient lookup APIs for graph navigation without implementing traversal algorithms or business logic.

### Current Capabilities

- Stores every relationship.
- Stores outgoing edges.
- Stores incoming edges.
- Prevents duplicate relationships.
- Supports neighbor lookup.
- Supports relationship type filtering.
- Supports relationship existence checks.

### Strengths

Very good separation of responsibilities.

The graph only stores data.

No traversal logic.

No compliance logic.

No provider-specific logic.

### Weaknesses

No major architectural issues.

Potential future improvements:

- relationship indexing
- graph statistics
- relationship metadata queries

None are required for Attack Path Analysis v1.

### Attack Path Impact

Suitable as-is.

No changes required.

---

## File

graph/traversal.py

### Responsibility

Implements graph traversal algorithms.

Currently provides Breadth First Search.

### Current Capabilities

- Reachable resource discovery
- Cycle protection
- Breadth-first traversal

### Strengths

Excellent separation.

Traversal is independent of graph storage.

Algorithms are reusable.

### Weaknesses

Currently exposes only:

reachable_from()

Future attack analysis will eventually require:

- shortest_path()
- path_exists()
- enumerate_paths()
- traversal constraints

These are future enhancements.

### Attack Path Impact

Current BFS is sufficient for Attack Path Analysis v1.

No immediate changes required.

---

## File

graph/graph_query.py

### Responsibility

Public query interface over the graph runtime.

Acts as the abstraction layer between graph infrastructure and graph-aware consumers.

### Current Capabilities

Traversal

- reachable_resources()
- is_reachable()

Relationship queries

- outgoing()
- incoming()
- neighbors()
- relationships()
- has_relationship()

Resource queries

- resources_of_type()

Semantic queries

- resources_with_capability()
- resources_with_capabilities()
- resources_of_canonical_type()

Dependency queries

- has_dependency()

### Strengths

GraphQuery is now the primary public API.

Rules no longer need to know how graph traversal works.

Semantic filtering has started moving into the query layer.

### Weaknesses

Current queries only answer "what is reachable?"

They cannot answer:

- How was it reached?
- Which path was taken?
- What intermediate resources exist?
- Multiple possible paths.
- Shortest path.

These are required for Attack Path Analysis.

### Attack Path Impact

GraphQuery should become the primary interface consumed by the future Attack Path Engine.

Rather than returning only resources, future APIs should also expose graph paths.

No changes required yet.

This branch will determine the required API additions after the remaining architecture audit.

---

# Phase 1 Decision

RelationshipGraph architecture is approved.

GraphTraversal architecture is approved.

GraphQuery architecture is approved.

No refactoring is required before beginning Attack Path Analysis.

Future work should extend existing abstractions rather than replace them.
