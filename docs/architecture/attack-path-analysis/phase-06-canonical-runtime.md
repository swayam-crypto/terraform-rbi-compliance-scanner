# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---

# Phase 6 – Canonical Runtime Audit

## Goal

Audit the Canonical Runtime to determine whether the normalized resource
model is sufficient for provider-independent infrastructure analysis and
future cloud providers.

This phase evaluates the transformation pipeline from parser output to
canonical resources and determines whether any architectural refactoring
is required before implementing Attack Path Analysis.

---

# Files Audited

## models/

- platform.py
- provider.py
- source_location.py
- resolved_resource.py

## canonical/

- resource.py
- context.py
- attribute_mapper.py
- classifier.py
- builder.py
- pipeline.py
- exceptions.py

---

# Canonical Runtime Overview

Current transformation pipeline

Platform Parser

↓

ResolvedResource

↓

Canonical Pipeline

↓

CanonicalResource

↓

Relationship Resolver

↓

Relationship Graph

The pipeline cleanly separates infrastructure parsing from semantic
normalization.

---

# models/

## Platform

### Responsibility

Identifies the Infrastructure-as-Code platform that produced the
resource.

Examples

- Terraform
- CloudFormation
- Pulumi
- Kubernetes
- Bicep

### Strengths

Provider-independent.

Future-proof.

No cloud-provider assumptions.

### Decision

Approved.

---

## CloudProvider

### Responsibility

Identifies the cloud provider.

Examples

- AWS
- Azure
- GCP
- OCI
- Cloudflare

### Strengths

Simple.

Independent from platform.

Allows Terraform Azure and Bicep Azure to produce the same provider.

### Decision

Approved.

---

## SourceLocation

### Responsibility

Stores origin metadata for diagnostics and reporting.

Current information

- file path
- resource address
- line
- column

### Strengths

Completely separated from runtime logic.

Useful for reporting without leaking parser concerns into the canonical
model.

### Decision

Approved.

---

## ResolvedResource

### Responsibility

Represents normalized parser output.

Acts as the boundary between platform-specific parsing and the canonical
cloud model.

### Current Contents

- platform
- provider
- resource_type
- resource_name
- attributes
- default_attributes
- source

### Strengths

Platform-independent.

Provider-aware.

Contains raw provider attributes without semantic interpretation.

Provides a consistent input model for every parser.

### Weaknesses

None identified.

The class intentionally represents parser output rather than semantic
cloud concepts.

It should not contain canonical capabilities or canonical types.

### Attack Path Impact

Attack Path Analysis should never consume ResolvedResource directly.

It should operate on CanonicalResource or later runtime abstractions.

### Decision

Approved.

No renaming required.

---

# canonical/

## CanonicalContext

### Responsibility

Shared transformation state for the Canonical Pipeline.

Each stage enriches the context before the final resource is built.

### Strengths

Pipeline stages remain independent.

Allows additional transformation stages in the future.

### Decision

Approved.

---

## CanonicalAttributeMapper

### Responsibility

Maps provider-specific attribute names into canonical attribute names.

Example

Terraform

↓

bucket

↓

canonical.storage_name

### Strengths

Catalog-driven.

No provider-specific logic exists in the mapper.

### Decision

Approved.

---

## ResourceClassifier

### Responsibility

Determines the canonical cloud type for a resource.

Semantic knowledge is delegated entirely to the Catalog.

### Strengths

Stateless.

Simple.

No hardcoded provider logic.

### Decision

Approved.

---

## CanonicalResourceBuilder

### Responsibility

Constructs immutable CanonicalResource instances.

### Strengths

Single responsibility.

Builder performs no semantic reasoning.

### Decision

Approved.

---

## CanonicalPipeline

### Responsibility

Coordinates canonical transformation.

Current stages

Catalog Lookup

↓

Canonical Context

↓

Attribute Mapping

↓

Builder

↓

Canonical Resource

### Strengths

Very clear orchestration.

Every stage owns one responsibility.

Easy to extend without modifying existing stages.

### Weaknesses

None identified.

### Decision

Approved.

---

## CanonicalResource

### Responsibility

Represents provider-independent semantic cloud infrastructure.

Current Contents

- platform
- provider
- canonical_type
- resource_name
- canonical attributes
- capabilities
- metadata
- source

### Strengths

Exactly the abstraction higher layers should consume.

No provider-specific attributes remain.

Capabilities are attached.

Canonical type is attached.

Ready for graph reasoning.

### Attack Path Impact

Attack Path Analysis should consume the graph runtime rather than
parser output.

The graph currently stores ResolvedResource instances.

Future architectural evolution may introduce CanonicalResource-backed
graphs, however this is intentionally outside the scope of the current
implementation.

### Decision

Approved.

---

# Architectural Observation

One important architectural distinction became clear during this audit.

ResolvedResource and CanonicalResource represent different stages of the
pipeline.

ResolvedResource

↓

Normalized parser output

CanonicalResource

↓

Semantic cloud model

These are not interchangeable.

They should remain separate types.

---

# Refactoring Assessment

Earlier consideration

Rename ResolvedResource to CanonicalResource.

Audit Result

Rejected.

Reason

The project already has a clear separation between:

Parser Runtime

↓

ResolvedResource

Semantic Runtime

↓

CanonicalResource

Renaming would reduce clarity rather than improve it.

---

# Attack Path Impact

Attack Path Analysis should begin after CanonicalResource has been
constructed.

It should never depend on parser-specific resource types or provider
attributes.

The attack engine should consume only:

- CanonicalResource
- RelationshipGraph
- GraphQuery
- Catalog capabilities

---

# Decision

Canonical Runtime is approved.

No architectural refactoring is required before implementing Attack Path
Analysis.

The Canonical Cloud Model successfully separates parser concerns from
semantic infrastructure modelling and provides a stable foundation for
future providers and higher-level analysis engines.