# Attack Path Analysis Architecture

## Overview

This directory contains the architectural audit and design documents for
the Attack Path Analysis initiative.

Rather than implementing the feature immediately, the existing platform
was audited to determine whether its architecture could support an
Attack Path Engine without requiring major refactoring.

The audit covered every major architectural layer of the compliance
scanner, including the graph runtime, semantic layer, canonical runtime,
rule engine and knowledge base.

The result of the audit was that the current architecture already
provides a strong foundation for Attack Path Analysis.

No significant architectural redesign was required.

Instead, Attack Path Analysis will be implemented as a new
infrastructure analysis capability that builds upon the existing
architecture.

---

# Audit Goals

The audit was performed to answer the following questions:

- Is the graph runtime sufficient for attack path analysis?
- Is the relationship model extensible?
- Is the semantic layer provider-independent?
- Does the canonical runtime require redesign?
- Is the rule architecture scalable?
- Is the knowledge base expressive enough for infrastructure analysis?
- What architectural changes are required before implementation?

---

# Architecture Principles

The audit follows several architectural principles that should continue
to guide future development.

## Separation of Responsibilities

Infrastructure parsing, semantic modelling, infrastructure analysis and
compliance evaluation remain separate concerns.

---

## Provider Independence

Infrastructure analysis should reason about canonical cloud concepts
rather than provider-specific resource types.

Examples include:

- Canonical Types
- Capabilities
- Graph Relationships

The analysis layer should never depend directly on AWS-specific resource
names.

---

## Reusable Infrastructure Analysis

Attack Path Analysis is the first implementation of a reusable
Infrastructure Analysis Layer.

Future analysis engines should be able to consume the same runtime
artifacts without requiring architectural redesign.

Examples include:

- Risk Analysis
- Blast Radius Analysis
- Lateral Movement Analysis
- Privilege Escalation Analysis
- Evidence Generation

---

# Audit Documents

## Phase 1

Graph Foundation

Reviews the graph data structure, traversal algorithms and graph query
abstractions.

---

## Phase 2

Relationship Resolution

Reviews relationship extraction and graph construction.

---

## Phase 3

Semantic Layer

Reviews the catalog API and semantic abstractions used throughout the
platform.

---

## Phase 4

Runtime

Reviews the scan pipeline, execution flow and runtime orchestration.

---

## Phase 5

Rules & Compliance

Reviews the compliance rule architecture and the integration of graph
analysis into rule execution.

---

## Phase 6

Canonical Runtime

Reviews the canonical cloud model, transformation pipeline and runtime
resource representation.

---

## Phase 7

Knowledge Base

Reviews the provider-independent knowledge base that defines canonical
resource semantics, capabilities and relationships.

---

## Phase 8

Attack Path Analysis Architecture

Defines the implementation architecture for the Attack Path Engine and
its integration into the existing platform.

---

# Audit Outcome

The architectural audit concludes that the existing platform already
provides a mature and extensible foundation for Attack Path Analysis.

The following components were approved without requiring architectural
redesign:

- Graph Runtime
- Relationship Resolution
- Semantic Layer
- Runtime Pipeline
- Compliance Rule Architecture
- Canonical Runtime
- Knowledge Base

Future work should focus on implementing new analysis capabilities
rather than restructuring the existing architecture.

---

# Future Vision

The long-term vision of the platform is to provide a reusable
Infrastructure Analysis Layer capable of supporting multiple forms of
cloud infrastructure analysis.

The Attack Path Engine represents the first analysis engine built upon
this architecture.

Future engines should integrate with the same graph runtime and semantic
knowledge base while preserving the architectural principles established
through this audit.