# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---
# Phase 3 - Semantic Layer Audit

---

## Files

catalog/catalog.py

catalog/models.py

catalog/canonical_types.py

---

## Responsibility

The Catalog is the semantic knowledge base of the platform.

It translates provider-specific resources into provider-independent concepts that every higher layer can reason about.

The graph answers:

> "How are resources connected?"

The catalog answers:

> "What are these resources?"

Attack Path Analysis requires both.

---

## Current Capabilities

### Resource Classification

Every resource exposes:

- provider
- service
- canonical_type
- kind

allowing provider-independent reasoning.

### Capability Model

Resources expose capabilities through:

```
capabilities
```

Current queries allow:

- has_capability()
- has_capabilities()

This is the first abstraction Attack Path Analysis should consume.

### Semantic Queries

Catalog already provides:

- canonical_type()
- provider()
- service()
- aliases()
- relationships()

GraphQuery already consumes part of this information.

---

## Canonical Types

Current canonical types already classify almost every attack-path component.

Examples:

Compute

- virtual_machine
- serverless_function
- container_cluster
- container_service

Networking

- load_balancer
- api_gateway
- vpc
- subnet
- security_group

Storage

- object_storage
- block_storage
- file_storage

Data

- database
- cache
- message_queue

Security

- secret
- kms_key
- iam_role
- iam_policy

This is sufficient for Attack Path Analysis v1.

No additional canonical types are required.

---

## ResourceDefinition

ResourceDefinition currently contains:

Identity

- provider
- service

Classification

- canonical_type
- kind

Semantics

- capabilities

Compliance

- attributes

Relationships

- relationships

Metadata

- metadata

This model is well separated.

No attack-specific information has leaked into the semantic layer.

---

## Strengths

Excellent separation.

The semantic layer describes infrastructure.

It does not perform analysis.

It does not contain attack logic.

It does not contain compliance logic.

It simply classifies infrastructure.

Exactly what we want.

---

## Weaknesses

Attack Path Analysis cannot yet answer questions like:

- Is this resource externally reachable?

- Is this a high-value target?

- Is this an execution environment?

- Does this represent a trust boundary?

These concepts currently depend on capabilities defined in the catalog.

The semantic layer itself does not model attack semantics.

---

## Attack Path Impact

Attack Path Analysis should **never classify resources itself.**

Instead it should consume the semantic information already provided by the catalog.

Example

Attack engine should ask:

- resources_with_capability("public_entry_point")

NOT

- resource.resource_type == "aws_lb"

Likewise:

Attack engine should ask:

- resources_of_canonical_type(DATABASE)

NOT

- aws_db_instance
- azurerm_postgresql_server
- google_sql_database_instance

This keeps Attack Path Analysis provider-independent.

---

## Future Extensions

The catalog may eventually define additional capabilities such as:

- internet_reachable
- execution_environment
- identity_provider
- trust_boundary
- administrative_access
- privilege_boundary

These belong in the catalog, not in the Attack Path Engine.

Attack Path Analysis should simply consume them.

---

# Phase 3 Decision

The semantic layer is approved.

No architectural changes are required before implementing Attack Path Analysis.

The attack engine should rely exclusively on:

- GraphQuery
- Catalog capabilities
- Canonical types

It should not contain provider-specific knowledge.

It should not duplicate semantic classification already present in the catalog.
