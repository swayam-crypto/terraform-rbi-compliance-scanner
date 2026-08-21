# Phase 02 – Canonical Architecture Review

**Project:** Cloud Compliance Intelligence Platform

**Version:** v0.10.0

**Status:** Complete

---

# Objective

Evaluate the canonical cloud model and determine whether it provides a suitable foundation for the long-term runtime architecture of the platform.

This review focuses on the relationship between:

- Parser models
- Canonical models
- Catalog
- Resource definitions

The goal is to understand the current architectural state without introducing implementation changes.

---

# Scope

Reviewed packages:

- canonical/
- catalog/
- models/

Not reviewed:

- Runtime
- Graph
- Attack
- Rules

These components were evaluated during Phase 01.

---

# Current Architecture

Current canonical pipeline:

Infrastructure Parser

↓

ResolvedResource

↓

Canonical Pipeline

↓

CanonicalResource

The catalog provides semantic definitions that drive the canonical transformation process.

The runtime currently continues operating on `ResolvedResource`.

---

# Architectural Responsibilities

## Parser

Responsible for converting provider-specific infrastructure into a common parser representation.

Primary runtime object:

- ResolvedResource

---

## Catalog

Responsible for describing cloud resources.

Current responsibilities include:

- Canonical types
- Resource kinds
- Capabilities
- Attributes
- Aliases
- Relationships
- Metadata

The catalog contains platform knowledge but does not contain runtime behavior.

---

## Canonical Pipeline

Responsible for transforming parser resources into canonical resources.

The pipeline is composed of several independent stages:

- Classification
- Attribute mapping
- Resource construction

The pipeline remains focused on transformation and does not perform graph analysis or compliance evaluation.

---

## Canonical Resource

Represents a provider-independent description of a cloud resource.

Current contents include:

- Canonical type
- Kind
- Capabilities
- Attributes
- Metadata

The model is immutable and intentionally lightweight.

---

# Strengths

## Clear Separation of Responsibilities

The parser, catalog, and canonical pipeline have well-defined responsibilities.

The parser extracts infrastructure.

The catalog provides semantic definitions.

The canonical pipeline performs transformation.

---

## Data-Driven Architecture

Cloud knowledge resides within the catalog instead of application logic.

Adding or modifying cloud resource definitions primarily requires catalog changes rather than runtime modifications.

This architecture supports long-term provider expansion.

---

## Pipeline Design

The canonical transformation pipeline is decomposed into small components with single responsibilities.

This improves maintainability and extensibility.

---

## Immutable Domain Models

Canonical resources and catalog definitions are immutable.

This reduces unintended state mutation during runtime processing.

---

# Observations

## CanonicalResource is currently a transformation output

The canonical pipeline successfully produces provider-independent resources.

However, these resources are not yet the primary runtime model.

The runtime continues operating on ResolvedResource.

This is an architectural observation rather than an implementation defect.

---

## Runtime Ownership is currently undefined

The review identified an unresolved architectural question.

Current runtime components operate on:

- ResolvedResource

The canonical pipeline produces:

- CanonicalResource

The long-term ownership of the runtime model has not yet been explicitly defined.

The current architecture supports either approach but has not committed to one.

---

## Catalog acts as the semantic center of the platform

The catalog owns resource semantics.

The canonical pipeline intentionally contains very little cloud-specific knowledge.

This separation is considered a strength.

---

## Relationship Definitions

The catalog defines relationship metadata.

The runtime constructs graph relationships independently.

These represent different concepts:

- Catalog relationships describe expected cloud semantics.
- Runtime relationships describe actual infrastructure connections.

This distinction should remain clearly documented.

---

# Architectural Risks

## Runtime Model Ambiguity

The platform currently contains two important resource models:

- ResolvedResource
- CanonicalResource

The long-term responsibilities of each model have not yet been finalized.

Future runtime evolution depends on resolving this question.

---

## Future Runtime Evolution

Future analysis engines may include:

- Attack analysis
- Blast radius analysis
- Identity analysis
- Risk analysis

The review does not recommend implementation changes at this stage.

However, future architectural work should clearly define which resource model these analyses operate on.

---

# Technical Debt Identified

## AD-007

Runtime ownership between ResolvedResource and CanonicalResource remains undefined.

Priority:

High

---

## AD-008

Public catalog APIs currently operate on ResolvedResource.

If CanonicalResource becomes the runtime model, catalog interfaces may require architectural review.

Priority:

Medium

---

# Recommendations

## Immediate

No implementation changes are recommended.

The current canonical architecture is internally consistent.

---

## Short-Term

Document the intended responsibilities of:

- ResolvedResource
- CanonicalResource

This decision should precede major runtime evolution.

---

## Medium-Term

Produce an architectural RFC describing Runtime V2.

The RFC should define:

- Runtime ownership
- Resource model ownership
- Runtime boundaries
- Canonical model responsibilities

Implementation should follow the approved architecture.

---

# Verdict

The canonical architecture is well structured and demonstrates clear separation between transformation logic and cloud knowledge.

The catalog is one of the strongest architectural components of the platform and provides a solid foundation for provider-independent resource modeling.

The primary architectural question identified during this review is not related to implementation quality.

Instead, it concerns long-term runtime ownership.

The platform has successfully introduced a provider-independent canonical model.

However, the runtime currently continues operating on the parser model.

Whether the runtime should eventually migrate to CanonicalResource remains an open architectural decision.

This review recommends documenting that decision before introducing additional runtime analysis engines.

---

# Debt Added

- AD-007
- AD-008

---

# Next Phase

Phase 03 – Catalog Architecture Review

Scope:

- Catalog definitions
- YAML schema
- Resource modeling
- Attribute specifications
- Relationship definitions
- Provider extensibility