# Phase 03 – Graph Runtime Architecture Review

**Project:** Cloud Compliance Intelligence Platform

**Version:** v0.10.0

**Status:** Complete

---

# Objective

Evaluate the graph runtime architecture and determine whether it provides a suitable foundation for infrastructure analysis.

This review focuses on:

- Relationship Graph
- Graph Construction
- Graph Traversal
- Graph Query Layer
- Graph Predicates
- Graph Rules
- Attack Path Analysis
- Runtime Integration

The objective is to determine whether the graph subsystem can support future platform capabilities including attack analysis, blast radius analysis, identity analysis, and AI-assisted infrastructure reasoning.

---

# Scope

Reviewed packages:

- graph/
- graph_rules/
- attack/
- rules/graph_base.py
- rules/kms_dependency.py
- rules/registry.py
- scan_context.py
- core/scan_engine.py

---

# Current Architecture

Current runtime graph pipeline:

Infrastructure Parser

↓

Relationship Resolver

↓

Relationship Graph

↓

Scan Context

↓

Attack Analysis

↓

Graph Rules

↓

Compliance Findings

The runtime constructs the graph once and shares it across all graph-based analyses.

---

# Architectural Responsibilities

## Relationship Graph

Responsible for representing infrastructure topology.

Responsibilities include:

- Relationship storage
- Incoming edge lookup
- Outgoing edge lookup
- Resource connectivity

The graph does not perform business analysis.

---

## Graph Traversal

Responsible for graph navigation algorithms.

Current implementation provides reusable traversal functionality without introducing compliance-specific logic.

Traversal remains independent of higher-level analyses.

---

## Graph Query

Responsible for exposing graph operations through higher-level query methods.

Graph consumers interact with query abstractions rather than graph internals.

This reduces duplication across runtime analyses.

---

## Graph Predicates

Responsible for expressing business-oriented graph conditions.

Predicates translate infrastructure questions into reusable graph queries.

Examples include dependency and capability-based predicates.

The predicate layer separates graph mechanics from compliance reasoning.

---

## Graph Rules

Responsible for evaluating graph-based compliance conditions.

Graph rules consume runtime graph abstractions rather than implementing graph algorithms directly.

---

## Attack Analysis

Responsible for discovering attack paths across infrastructure.

Attack analysis operates independently of compliance rules while sharing the same graph runtime.

The subsystem is layered as:

Attack Engine

↓

Attack Finder

↓

Shortest Path Algorithm

↓

Relationship Graph

Each component has a clearly defined responsibility.

---

## Scan Context

Responsible for sharing runtime state.

Current runtime state includes:

- Resources
- Resource Index
- Relationship Graph
- Attack Paths

The context acts as the shared runtime container for graph-based analyses.

---

# Strengths

## Clear Layered Architecture

Graph functionality is divided into independent layers.

Relationship storage, traversal, querying, predicates, and rule evaluation each have distinct responsibilities.

This separation improves maintainability and extensibility.

---

## Single Graph Ownership

The runtime constructs the infrastructure graph once.

Graph ownership remains centralized.

Graph consumers never rebuild infrastructure topology.

This reduces duplication and ensures consistent runtime analysis.

---

## Reusable Analysis Foundation

The graph runtime is not limited to compliance rules.

The same graph can support multiple independent analyses including:

- Attack Analysis
- Blast Radius Analysis
- Identity Analysis
- Risk Analysis
- AI-assisted Infrastructure Reasoning

The architecture naturally supports future analysis engines.

---

## Strong Runtime Separation

The runtime orchestrates analysis.

Individual subsystems own implementation details.

Graph construction, attack analysis, and graph rules remain independent while sharing common runtime state.

---

## Attack Analysis Integration

Attack analysis is implemented as an independent runtime analysis.

It consumes graph information without introducing graph-specific logic into the runtime orchestration layer.

This separation provides a reusable architecture for future runtime analyses.

---

# Observations

## Graph is Infrastructure

The graph package intentionally avoids business-specific logic.

Business reasoning exists in:

- Graph Predicates
- Graph Rules
- Attack Analysis

This separation is considered an architectural strength.

---

## Runtime Owns Orchestration

The scan engine coordinates runtime execution.

Individual analysis engines remain responsible only for their own domain logic.

The runtime does not perform graph reasoning directly.

---

## Scan Context is Becoming the Runtime Container

The ScanContext has evolved into the shared runtime object.

Future analyses are expected to extend this context rather than introducing additional runtime state containers.

This evolution is considered natural for the current platform architecture.

---

# Architectural Risks

## Runtime Growth

Future runtime analyses may include:

- Blast Radius
- Identity
- Privilege
- Risk
- AI Analysis

As the number of analyses increases, runtime orchestration may eventually benefit from a dedicated analysis pipeline.

This is considered future evolution rather than current architectural debt.

---

# Technical Debt Identified

No new architectural debt was identified during Phase 03.

The review confirms that graph ownership, runtime integration, and attack analysis boundaries are clearly defined.

---

# Recommendations

## Immediate

No architectural refactoring is recommended.

The graph runtime architecture provides a strong foundation for future platform capabilities.

---

## Medium-Term

As additional runtime analyses are introduced, evaluate whether runtime orchestration should transition toward an Analysis Pipeline or similar abstraction.

Such a transition should preserve the current separation between orchestration and analysis engines.

---

# Verdict

The graph runtime is the strongest architectural subsystem reviewed so far.

The architecture demonstrates excellent separation between infrastructure representation, graph traversal, business predicates, compliance rules, and attack analysis.

Graph construction has a single owner.

Graph consumers remain independent.

Runtime orchestration is centralized without introducing analysis-specific logic.

The subsystem provides a reusable analytical foundation capable of supporting future runtime capabilities beyond compliance scanning.

No major architectural weaknesses were identified during this review.

---

# Debt Added

None.

---

# ADR Changes

None.

The review validates previously documented architectural decisions and does not introduce new architectural decisions.

---

# Next Phase

Phase 04 – Rule Engine Architecture

Scope:

- Rule framework
- Rule registry
- Rule execution pipeline
- Compliance engine
- Finding generation
- Rule extensibility