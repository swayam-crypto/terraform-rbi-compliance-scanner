# Canonical Runtime Architecture

## Status

Current implementation after completion of the Canonical Cloud Model.

This document describes the execution flow of the scanner, the responsibilities of each architectural component, and the boundaries between subsystems.

---

# High-Level Architecture

```text
                    Terraform Files
                           │
                           ▼
                  Terraform Parser
                           │
                           ▼
                   ResolvedResource[]
                           │
                           ▼
                 Compliance Scan Engine
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
     Compliance Rules   ResourceIndex   RelationshipExtractor
            │              │              │
            │              ▼              ▼
            │       RelationshipGraph ◄──┘
            │
            ▼
         Findings


Canonical Cloud Model

ResolvedResource
        │
        ▼
CanonicalPipeline
        │
        ▼
CanonicalResource
```

The Canonical Cloud Model currently exists independently from the runtime and is not yet integrated into the scan execution flow.

---

# Current Runtime

## Terraform Parser

Responsibility

- Parse Terraform configuration and plans.
- Resolve provider defaults.
- Produce provider-specific `ResolvedResource` objects.

Output

```text
list[ResolvedResource]
```

---

## ResolvedResource

Represents a provider-specific cloud resource.

Contains

- provider
- platform
- resource_type
- resource_name
- provider attributes
- provider defaults
- source location

This is currently the primary runtime model.

---

## Compliance Scan Engine

Primary orchestrator of the runtime.

Responsibilities

- Receive parser output.
- Execute resource rules.
- Build resource index.
- Extract relationships.
- Build graph.
- Execute graph rules.
- Return findings.

Current flow

```text
ResolvedResource[]

↓

Resource Rules

↓

Relationship Extraction

↓

Relationship Graph

↓

Graph Rules

↓

Findings
```

---

# Rule System

Rules currently consume

```text
ResolvedResource
```

Rules determine applicability through

- catalog capability lookup
- provider resource type

Rules access attributes using

```text
catalog.attribute_name(...)
```

followed by

```text
resource.get(...)
```

This means rules remain provider-aware through catalog lookups.

---

# Resource Index

Purpose

Provide deterministic lookup across resources.

Stores

```text
ResolvedResource
```

Supports

- lookup by type
- lookup by name
- lookup by type + name

Used by

- RelationshipExtractor
- Graph Rules

---

# Relationship Extraction

Purpose

Build semantic relationships between resources.

Input

```text
ResolvedResource[]
```

Uses

- Catalog relationship definitions
- Terraform attribute references

Produces

```text
Relationship[]
```

Current relationship model

```text
Relationship

source -> ResolvedResource

target -> ResolvedResource

relationship_type
```

---

# Relationship Graph

Purpose

Provide graph traversal for graph-aware rules.

Constructed by

```text
GraphBuilder
```

Consumes

```text
Relationship[]
```

---

# Graph Rules

Graph rules operate on

```text
ScanContext
```

which currently contains

- ResolvedResource[]
- ResourceIndex
- RelationshipGraph

---

# Canonical Cloud Model

Purpose

Provide a provider-independent semantic representation of cloud resources.

Pipeline

```text
ResolvedResource

↓

Catalog Definition

↓

CanonicalContext

↓

CanonicalAttributeMapper

↓

CanonicalResourceBuilder

↓

CanonicalResource
```

---

# Canonical Resource

Contains

- platform
- provider
- canonical_type
- resource_name
- canonical attributes
- capabilities
- metadata
- source

Canonical resources are immutable.

---

# Current Separation

Parser

↓

ResolvedResource

↓

Runtime

↓

Findings


Canonical Cloud Model

↓

CanonicalResource

There is currently no integration point between these two systems.

---

# Current Runtime Dependencies

Parser

↓

ResolvedResource

↓

Scan Engine

↓

Rules

↓

Graph

↓

Findings


Canonical Pipeline

↓

CanonicalResource

The Canonical Pipeline is currently independent of runtime execution.

---

# Architectural Strengths

- Clear parser/runtime separation.
- Immutable CanonicalResource model.
- Catalog-driven semantic mapping.
- Provider-independent canonical type system.
- Attribute mapping isolated from rule logic.
- Relationship definitions stored in catalog.
- Graph subsystem isolated from parser.

---

# Current Architectural Gap

The runtime operates entirely on `ResolvedResource`.

The Canonical Cloud Model produces `CanonicalResource`.

No runtime component currently consumes canonical resources.

As a result:

- Rules evaluate provider-specific resources.
- ResourceIndex indexes provider-specific resources.
- RelationshipGraph contains provider-specific resources.
- Graph rules operate on provider-specific resources.

The Canonical Cloud Model is currently disconnected from runtime execution.

---

# Open Design Question

The next architectural decision is determining where canonical resources should enter the runtime.

Possible integration points include

- before runtime execution
- inside runtime orchestration
- during graph construction
- during rule evaluation

This decision should be made before implementing further architectural changes.

---
# Runtime Migration Strategy

## Objective

The Canonical Cloud Model has been implemented and is capable of transforming
provider-specific `ResolvedResource` objects into provider-independent
`CanonicalResource` objects.

The current runtime, however, still executes entirely on
`ResolvedResource`.

The objective of the runtime refactor is to establish
`CanonicalResource` as the single execution model used by the compliance
engine while preserving existing runtime behavior.

---

# Runtime Boundary

The runtime begins after Terraform parsing has completed.

Current boundary:

```text
Terraform Files
        │
        ▼
Terraform Parser
        │
        ▼
ResolvedResource
──────────────────────────────────── Runtime Boundary
        │
        ▼
Scan Engine
```

Target boundary:

```text
Terraform Files
        │
        ▼
Terraform Parser
        │
        ▼
ResolvedResource
        │
        ▼
Canonical Pipeline
        │
        ▼
CanonicalResource
──────────────────────────────────── Runtime Boundary
        │
        ▼
Compliance Runtime
```

The parser remains responsible for provider-specific normalization.

The runtime becomes entirely provider-independent.

---
# Canonical Boundary

The Canonical Boundary separates provider-specific infrastructure
representation from the provider-independent compliance runtime.

Every infrastructure definition must cross this boundary exactly once.

```
Terraform Files
        │
        ▼
Terraform Parser
        │
        ▼
ResolvedResource
        │
        ▼
Canonical Pipeline
──────────────────────────────────────────────
            CANONICAL BOUNDARY
──────────────────────────────────────────────
        │
        ▼
CanonicalResource
        │
        ▼
Compliance Runtime
```

Above the Canonical Boundary:

- Provider-specific interpretation is allowed.
- Parser-specific syntax is allowed.
- Provider defaults may exist.
- Resource classification may occur.
- Attribute mapping may occur.

Below the Canonical Boundary:

- Runtime components operate only on semantic cloud objects.
- Runtime components must not interpret provider-specific resource types.
- Runtime components must not resolve provider-specific attribute names.
- Runtime components must not parse infrastructure syntax.
- Runtime components evaluate infrastructure using only semantic models.
---
# Runtime Execution Model

Current runtime execution:

```text
ResolvedResource[]
        │
        ▼
Scan Engine
        │
        ├──────────────► Resource Rules
        │
        ├──────────────► ResourceIndex
        │
        ├──────────────► RelationshipExtractor
        │
        ├──────────────► GraphBuilder
        │
        └──────────────► Graph Rules
```

Target runtime execution:

```text
ResolvedResource[]
        │
        ▼
Canonical Pipeline
        │
        ▼
CanonicalResource[]
        │
        ▼
Scan Engine
        │
        ├──────────────► Resource Rules
        │
        ├──────────────► ResourceIndex
        │
        ├──────────────► RelationshipExtractor
        │
        ├──────────────► GraphBuilder
        │
        └──────────────► Graph Rules
```

The runtime should no longer depend on provider-specific resource models.

---

# Runtime Responsibilities

## Parser Layer

Owns:

- Terraform parsing
- Provider resolution
- Default value resolution
- Construction of `ResolvedResource`

The parser is the only subsystem that should understand provider-specific
resource types.

---

## Canonical Cloud Model

Owns:

- Resource classification
- Canonical type resolution
- Attribute mapping
- Metadata normalization
- Construction of immutable `CanonicalResource`

The Canonical Cloud Model defines the provider-independent semantic
representation of cloud infrastructure.

---

## Runtime Layer

Owns:

- Resource indexing
- Relationship extraction
- Relationship graph construction
- Compliance rule execution
- Graph rule execution
- Finding generation

The runtime should operate exclusively on `CanonicalResource`.

---

# Runtime Data Model

Current runtime model:

```text
ResolvedResource
```

Target runtime model:

```text
CanonicalResource
```

`ResolvedResource` is a parser implementation detail and should not
propagate beyond the Canonical Pipeline.

`CanonicalResource` becomes the single runtime representation used by
all runtime components.

---

# Architectural Principles

The runtime refactor follows these principles.

## Provider Independence

Runtime components must not depend on provider-specific resource types or
provider-specific attribute names.

All provider-specific knowledge is resolved before runtime execution begins.

---

## Single Runtime Model

The runtime should expose exactly one resource representation.

Multiple runtime models increase coupling and require duplicated logic.

The Canonical Cloud Model establishes `CanonicalResource` as the canonical
runtime representation.

---

## Layer Responsibilities

Parser Layer

- Provider-specific

Canonical Cloud Model

- Semantic transformation

Runtime Layer

- Compliance evaluation

Each layer owns one responsibility.

---
# Runtime Contract

The Compliance Runtime operates exclusively on semantic cloud models.

Every runtime component assumes that semantic normalization has already
been completed by the Canonical Pipeline.

Runtime components may rely on:

- CanonicalType
- canonical attributes
- semantic capabilities
- semantic metadata
- source location

Runtime components must never rely on:

- Terraform resource types
- CloudFormation resource types
- Pulumi resource types
- provider-specific attribute names
- provider defaults
- parser-specific syntax

If a runtime component requires provider-specific information, that
information belongs above the Canonical Boundary.
---
# Migration Scope

The runtime refactor changes the internal execution model only.

It does not introduce:

- new compliance rules
- new cloud providers
- new runtime features
- new scanning behavior

Existing functionality should remain behaviorally identical after the
migration.

---

# Expected Runtime

```text
Terraform Files
        │
        ▼
Terraform Parser
        │
        ▼
ResolvedResource
        │
        ▼
Canonical Pipeline
        │
        ▼
CanonicalResource
        │
        ▼
ScanContext
        │
        ├────────► ResourceIndex
        ├────────► RelationshipExtractor
        ├────────► RelationshipGraph
        ├────────► Resource Rules
        └────────► Graph Rules
                │
                ▼
             Findings
```
---
## Status

### Completed

- Canonical Cloud Model
- Canonical Pipeline
- Canonical Attribute Mapping
- Canonical Resource Construction

### In Progress

- Runtime migration to CanonicalResource

### Pending

- Rule migration
- Graph rule migration
- Runtime cleanup
---
# Long-Term Vision

The long-term architecture of the platform follows four logical layers.

```
Parser Layer
        │
        ▼
Normalization Layer
        │
        ▼
Semantic Layer
        │
        ▼
Compliance Runtime
```

Parser Layer

- Parses infrastructure definitions.
- Produces normalized infrastructure models.

Semantic Layer

- Classifies resources.
- Maps provider-specific attributes.
- Resolves semantic capabilities.
- Produces CanonicalResource.

Compliance Runtime

- Executes compliance rules.
- Builds resource graphs.
- Evaluates graph rules.
- Produces findings.

Each layer has exactly one responsibility.

The runtime should never perform semantic interpretation.

Semantic interpretation belongs entirely to the Canonical Cloud Model.