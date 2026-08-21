# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---

# Phase 7 – Knowledge Base Audit

## Goal

Audit the Catalog Knowledge Base to determine whether the semantic
resource definitions provide a sufficient foundation for provider-
independent infrastructure analysis.

This phase evaluates whether the catalog can support higher-level
analysis engines such as Graph Query, Attack Path Analysis and future
Risk Analysis without requiring provider-specific logic.

---

# Files Audited

catalog/data/aws/

- analytics.yaml
- aws.yaml
- baseline.yaml
- compute.yaml
- database.yaml
- identity.yaml
- messaging.yaml
- monitoring.yaml
- networking.yaml
- security.yaml
- storage.yaml

---

# Knowledge Base Overview

The catalog is not simply a collection of provider mappings.

The Catalog should be treated as infrastructure knowledge rather than
configuration.

Its primary purpose is to describe cloud concepts, relationships and
behaviour in a provider-independent manner.

Higher-level analysis engines consume this knowledge without embedding
provider-specific logic.

It is the semantic knowledge base of the platform.

Its responsibilities are to describe:

- canonical cloud resources
- canonical capabilities
- canonical relationships
- canonical attributes
- provider aliases

Every higher-level subsystem consumes this knowledge.

Current architecture

Provider Resource

↓

Catalog Definition

↓

Canonical Cloud Model

↓

Relationship Resolution

↓

Relationship Graph

↓

Graph Query

↓

Attack Path Analysis

↓

Compliance Rules

The knowledge base therefore forms the semantic foundation of the
entire platform.

---

# Resource Definitions

Each resource definition currently provides:

- provider
- service
- canonical type
- resource kind
- capabilities
- canonical attributes
- relationships
- aliases
- metadata

This allows higher layers to reason about infrastructure without
requiring provider-specific logic.

---

# Canonical Types

Resource definitions consistently classify infrastructure into
provider-independent cloud concepts.

Examples include:

- Compute
- Database
- Object Storage
- Networking
- Identity
- Monitoring
- Security

Higher-level systems therefore reason about cloud concepts rather than
AWS resource names.

---

# Capability Model

Capabilities represent the behavior of a resource rather than its
implementation.

Examples include:

- public_entry_point
- data_store
- encryption_at_rest
- audit_logging

This abstraction allows analysis engines to answer semantic questions
without hardcoding provider-specific resource types.

Example

Instead of asking:

Is this resource aws_db_instance?

higher layers ask:

Does this resource provide the data_store capability?

This is the correct architectural abstraction.

---

# Relationship Definitions

Relationship metadata describes how resources connect to one another.

These definitions allow the Relationship Resolver to construct the
Relationship Graph without embedding provider-specific logic.

Graph construction therefore remains completely data-driven.

---

# Provider Independence

One of the primary objectives of the catalog is provider independence.

The current knowledge model successfully separates:

Platform

Terraform

Cloud Provider

AWS

Cloud Concept

Database

Future providers such as Azure, GCP or Kubernetes can therefore reuse
the same canonical concepts.

---

# Strengths

The catalog successfully separates infrastructure knowledge from
analysis.

Graph construction is entirely catalog-driven.

Canonical types provide stable semantic classification.

Capabilities provide reusable behavioral abstractions.

Relationships remain declarative.

Provider-specific knowledge is isolated inside the catalog.

The knowledge base is extensible without requiring runtime changes.

---

# Weaknesses

No architectural weaknesses were identified.

Current limitations relate only to catalog coverage.

Several cloud services have not yet been modeled.

This is expected and should be addressed by expanding the catalog
rather than modifying its architecture.

---

# Attack Path Impact

Attack Path Analysis should consume semantic knowledge exclusively from
the catalog.

It should never contain provider-specific resource names.

Instead it should reason entirely in terms of:

- canonical types
- capabilities
- graph relationships

This preserves provider independence and allows future cloud providers
to participate in attack-path analysis without modifying the analysis
engine.

---

# Future Expansion

Future work should extend the knowledge base by introducing additional
resource definitions.

Examples include:

Compute

- ECS
- EKS
- Fargate

Identity

- IAM Users
- IAM Roles
- IAM Groups

Security

- Secrets Manager
- Parameter Store
- WAF
- ACM

Networking

- Transit Gateway
- VPN Gateway
- PrivateLink

Monitoring

- CloudTrail
- GuardDuty
- Security Hub

These additions extend the catalog without requiring architectural
changes.

---

# Refactoring Assessment

None.

The existing knowledge model is well structured.

Future work should focus on expanding semantic coverage rather than
redesigning the catalog architecture.

---

# Decision

Approved.

The Catalog successfully functions as the semantic knowledge base of
the platform.

No architectural refactoring is required before implementing Attack
Path Analysis.

Future development should continue expanding the catalog while
preserving the existing provider-independent abstraction model.