# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---

# Phase 5 – Rules & Compliance Layer Audit

## Goal

Audit the rule architecture to determine how Attack Path Analysis should
integrate into the compliance engine without breaking the existing
separation of responsibilities.

This phase evaluates whether graph traversal should remain inside
individual graph rules or become a reusable runtime capability.

---

# Files Audited

## compliance/

- controls.py
- control_catalog.py
- baseline_controls.py

## rules/

- base.py
- catalog_rules.py
- baseline.py
- data_localization.py
- encryption.py
- audit_logging.py
- network_exposure.py
- access_control.py
- graph_base.py
- kms_dependency.py
- registry.py

## graph_rules/

- base.py
- public_database_exposure.py
- __init__.py

---

# Responsibilities

The Rules layer is responsible for evaluating compliance controls.

It determines whether infrastructure violates one or more compliance
requirements.

Rules should never be responsible for parsing infrastructure,
constructing graphs, or performing infrastructure analysis.

Instead, they should consume reusable runtime artifacts.

---

# Current Architecture

Current execution flow:

Terraform

↓

Parser

↓

Canonical Resources

↓

Relationship Resolver

↓

Relationship Graph

↓

Graph Rules

↓

Findings

Graph rules currently perform graph traversal directly through
GraphQuery and GraphPredicates.

---

# Compliance Layer

## Strengths

Compliance controls are completely framework-neutral.

Rules evaluate controls rather than embedding regulatory logic.

Framework mappings remain isolated inside the compliance package.

This separation allows multiple compliance frameworks to reuse the same
technical rule.

Example:

One encryption rule can satisfy:

- RBI
- DPDP
- CIS
- ISO 27001

without modifying the implementation.

---

# Rules Layer

## Strengths

Rules have a single responsibility:

Evaluate whether a control is satisfied.

Rules do not parse Terraform.

Rules do not resolve relationships.

Rules do not build graphs.

Rules already consume higher-level abstractions such as:

- Catalog
- GraphQuery
- GraphPredicates

This is a strong architectural boundary.

---

# Graph Rules

## Current Design

Graph rules currently receive:

ScanContext

↓

RelationshipGraph

↓

GraphQuery

↓

GraphTraversal

Every graph rule independently traverses the graph.

Example:

PublicDatabaseExposureRule

↓

GraphQuery

↓

Reachable Resources

↓

Compliance Finding

---

# Architectural Observation

The current implementation works correctly.

However, multiple graph rules will repeatedly perform similar graph
traversals.

As the number of graph rules increases this becomes duplicated work.

Examples:

Rule A

Internet

↓

Database

Rule B

Internet

↓

Secrets

Rule C

Internet

↓

Execution Environment

Each rule independently discovers the same attack paths.

---

# Attack Path Impact

Attack Path Analysis should become a reusable runtime capability.

Instead of:

Graph Rule

↓

GraphQuery

↓

Graph Traversal

the future runtime should become:

Relationship Graph

↓

Attack Path Engine

↓

Attack Path Collection

↓

Graph Rules

Attack-path-aware graph rules should consume reusable attack path results
rather than reconstructing graph traversal independently.

Relationship-based graph rules may continue using GraphQuery directly when
attack path analysis provides no additional value.
---

# Runtime Separation

RelationshipGraph

Responsible for:

- storing relationships

GraphTraversal

Responsible for:

- traversal algorithms

GraphQuery

Responsible for:

- querying graph data

AttackPathEngine

Responsible for:

- discovering attack paths

GraphRule

Responsible for:

- evaluating attack paths against compliance controls

This preserves single responsibility across every layer.

---

# Required Refactors

None.

The existing Rules architecture is approved.

Attack Path Analysis should be introduced as a new runtime capability
rather than modifying the existing rule abstractions.

---

# Future Runtime

Current

Relationship Graph

├── GraphQuery
│       ↓
│   Relationship Rules
│
└── AttackPathEngine
        ↓
AttackPathCollection
        ↓
Attack Path Rules

↓

Compliance Findings

This allows attack-path-aware graph rules to reuse the same attack-path
analysis while relationship-based graph rules continue using GraphQuery
directly.

---

# Decision

Approved.

No architectural refactoring is required before implementing Attack Path
Analysis.

The Rules layer should continue to use the abstraction most appropriate
for the rule being implemented.

Relationship-based rules should consume GraphQuery.

Attack-path-aware rules should consume AttackPathCollection.
---
## Rule Categories

Graph rules naturally fall into two categories.

### Relationship Rules

These evaluate direct infrastructure relationships.

Examples:

- Database depends on KMS
- Subnet belongs to VPC
- Load Balancer forwards to Target Group

These rules should continue using GraphQuery.

---

### Attack Path Rules

These evaluate exploitability through multiple infrastructure components.

Examples:

- Internet can reach Database
- Internet can reach Secret
- Public Compute can reach Internal Data Store

These rules should consume AttackPathCollection produced by the
AttackPathEngine.
---

# Notes

Attack Path Analysis is not a compliance rule.

It is an infrastructure analysis engine.

Compliance rules remain consumers of its output.

This distinction preserves the separation between infrastructure
analysis and compliance evaluation and provides a reusable foundation
for future capabilities such as:

- Risk Engine
- Evidence Engine
- Blast Radius Analysis
- Lateral Movement Analysis
- Attack Simulation