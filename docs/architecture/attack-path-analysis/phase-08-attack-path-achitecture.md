# Phase 8 – Attack Path Analysis Architecture

## Goal

Consolidate the findings from the previous architectural audits into a
single implementation blueprint for Attack Path Analysis.

Rather than introducing a new graph runtime or modifying the existing
Canonical Cloud Model, Attack Path Analysis will become a new
infrastructure analysis capability built on top of the existing
architecture.

This document defines the architectural boundaries, responsibilities,
runtime integration and implementation strategy for the
AttackPathEngine.

---

# Previous Audit Summary

The previous architectural audits produced the following conclusions.

| Phase | Decision |
|--------|----------|
| Phase 1 | Graph Foundation approved |
| Phase 2 | Relationship Resolution approved |
| Phase 3 | Semantic Layer approved |
| Phase 4 | Runtime approved |
| Phase 5 | Rules architecture approved |
| Phase 6 | Canonical Runtime approved |
| Phase 7 | Knowledge Base approved |

No architectural refactoring was identified as a prerequisite for
Attack Path Analysis.

The existing architecture provides a stable foundation.

---

# Architectural Vision

Attack Path Analysis is the first infrastructure analysis engine to be
introduced into the platform.

Its purpose is to reason about exploitability using the existing graph,
catalog and canonical cloud model.

Attack Path Analysis is not:

- a parser
- a graph
- a compliance rule
- a reporting component

It is an infrastructure analysis layer.

---

# Existing Architecture

Current runtime

Terraform

↓

Parser

↓

ResolvedResource

↓

Relationship Resolver

↓

Relationship Graph

↓

Graph Rules

↓

Findings

---

# Target Architecture

Terraform

↓

Parser

↓

ResolvedResource

↓

Relationship Resolver

↓

Relationship Graph

↓

GraphQuery

↓

AttackPathEngine

↓

AttackPathCollection

↓

Attack Path Rules

↓

Compliance Findings

---

# Architectural Layers

## Layer 1

Knowledge

Responsible for:

- canonical resource definitions
- capabilities
- canonical attributes
- relationships
- semantic classification

Components

- Catalog
- Canonical Types
- YAML Knowledge Base

---

## Layer 2

Infrastructure Runtime

Responsible for:

- parsing
- normalization
- relationship extraction
- graph construction

Components

- Parser
- ResolvedResource
- RelationshipResolver
- RelationshipGraph
- ScanContext

---

## Layer 3

Infrastructure Analysis

Responsible for analysing infrastructure.

Current analysis components

- GraphQuery

New analysis component

- AttackPathEngine

Future analysis components

- RiskEngine
- BlastRadiusEngine
- EvidenceEngine
- LateralMovementEngine

Analysis components consume runtime artifacts.

They never parse infrastructure.

---

## Layer 4

Compliance

Responsible for evaluating controls.

Components

- Resource Rules
- Relationship Rules
- Attack Path Rules

Compliance never performs infrastructure analysis.

It consumes reusable analysis produced by lower layers.

---

# Responsibilities

## RelationshipGraph

Stores graph data.

Never performs analysis.

---

## GraphTraversal

Provides traversal algorithms.

Never evaluates infrastructure.

---

## GraphQuery

Provides reusable graph queries.

Answers questions such as:

- What resources are reachable?
- Which resources have capability X?
- Which resources have canonical type Y?

GraphQuery remains useful even after Attack Path Analysis exists.

---

## AttackPathEngine

Consumes:

- RelationshipGraph
- GraphQuery
- Catalog

Produces:

AttackPathCollection

The engine performs infrastructure analysis only.

It does not evaluate compliance.

---

## AttackPathCollection

Represents reusable attack path analysis results.

Multiple compliance rules may consume the same collection.

Attack paths should never be recomputed by individual rules.

---

## Rules

Graph rules naturally fall into two categories.

### Relationship Rules

Evaluate direct infrastructure relationships.

Examples

- Database depends on KMS.
- Subnet belongs to VPC.
- Target Group attached to Load Balancer.

These rules consume GraphQuery.

---

### Attack Path Rules

Evaluate exploitability across multiple infrastructure components.

Examples

- Internet can reach Database.
- Internet can reach Secret.
- Public Compute can reach Internal Data Store.

These rules consume AttackPathCollection.

---

# Runtime Integration

Initial implementation

RelationshipGraph

↓

GraphQuery

↓

AttackPathEngine

↓

Tests

AttackPathEngine will initially be executed independently while its API
is stabilised.

Once the API has matured it may become part of ScanEngine.

This avoids introducing runtime coupling prematurely.

---

# Provider Independence

Attack Path Analysis must remain provider independent.

The engine must never identify resources using provider-specific
resource names.

Incorrect

aws_db_instance

Correct

CanonicalType.DATABASE

Incorrect

aws_lb

Correct

Capability("public_entry_point")

Infrastructure analysis must always consume:

- canonical types
- capabilities
- graph relationships

---

# Architectural Decisions

## Approved

- Existing Graph Runtime
- Existing Relationship Resolver
- Existing Catalog
- Existing Canonical Runtime
- Existing Rule Architecture

No redesign required.

---

## Rejected

### Embedding attack logic inside GraphQuery

Rejected.

GraphQuery provides graph queries.

AttackPathEngine performs infrastructure analysis.

---

### Embedding attack logic inside GraphRule

Rejected.

Rules consume analysis.

Rules do not perform infrastructure analysis.

---

### Renaming ResolvedResource

Rejected.

ResolvedResource represents parser output.

CanonicalResource represents semantic cloud infrastructure.

These are different runtime concepts.

---

# Future Expansion

The architecture intentionally supports future analysis engines.

Examples

- Risk Engine
- Blast Radius Analysis
- Lateral Movement Analysis
- Infrastructure Evidence Engine
- Privilege Escalation Analysis

These engines should consume the same graph runtime without requiring
architectural changes.

---

# Implementation Roadmap

Stage 1

Create AttackPathEngine.

Stage 2

Define AttackPath model.

Stage 3

Define AttackPathCollection.

Stage 4

Implement attack path discovery algorithms.

Stage 5

Create Attack Path Rules.

Stage 6

Integrate into ScanEngine.

---

# Final Decision

The architectural audit concludes that the current platform already
provides a sufficiently mature foundation for Attack Path Analysis.

No architectural refactoring is required.

Attack Path Analysis will be implemented as a new infrastructure
analysis engine that consumes the existing Canonical Cloud Model,
Relationship Graph and Catalog while preserving the current separation
between infrastructure modelling, infrastructure analysis and compliance
evaluation.