# CCIP Architecture Decisions

> This document records the major architectural decisions made during the evolution of CCIP.
>
> It is not an implementation guide.
>
> It explains *why* architectural decisions were made so future contributors understand the reasoning behind the platform.

---

# ADR-001

## Title

Canonical Cloud Model as the Core Platform

## Status

Accepted

## Version

v0.9.0

## Context

Prior to v0.9, compliance rules operated directly on `ResolvedResource`.

Although this worked for Terraform, it tightly coupled the compliance engine to provider-specific resource names and attributes.

Supporting additional cloud providers or Infrastructure-as-Code formats would require updating existing rules.

## Decision

Introduce the Canonical Cloud Model (CCM) as the semantic center of CCIP.

Infrastructure parsers continue producing `ResolvedResource`.

The Canonical Cloud Model transforms infrastructure into `CanonicalResource`.

Compliance rules consume `CanonicalResource`.

## Consequences

Positive

- Cloud-provider agnostic rules
- Infrastructure-as-Code agnostic rules
- Easier future expansion
- Better architecture separation

Negative

- Additional transformation step
- Slight runtime overhead
- Additional model to maintain

---

# ADR-002

## Title

Keep ResolvedResource

## Status

Accepted

## Version

v0.9.0

## Context

During architecture discussions, replacing `ResolvedResource` with `CanonicalResource` was considered.

## Decision

Do not replace `ResolvedResource`.

Instead:

Terraform

↓

ResolvedResource

↓

Canonical Cloud Model

↓

CanonicalResource

## Rationale

ResolvedResource represents parsed infrastructure.

CanonicalResource represents semantic infrastructure.

These are different responsibilities.

Keeping both maintains clean separation of concerns.

---

# ADR-003

## Title

CanonicalResource becomes the Rule Input

## Status

Accepted

## Version

v0.9.0

## Context

Historically, rules inspected provider-specific attributes.

This tightly coupled rule implementations to Terraform and cloud providers.

## Decision

Compliance rules will operate exclusively on `CanonicalResource`.

Rules should never depend on provider-specific resource names.

## Consequences

Adding Azure or Google Cloud support should require no rule modifications.

---

# ADR-004

## Title

Pipeline-Based Transformation

## Status

Accepted

## Version

v0.9.0

## Context

Normalization could be implemented as one large function.

## Decision

Implement the Canonical Cloud Model as a transformation pipeline.

Stages include:

- Resource Classification
- Canonical Mapping
- Attribute Normalization
- Capability Extraction
- Security Property Extraction
- Relationship Normalization
- Trace Generation

## Rationale

Each stage has one responsibility.

Stages become independently testable.

Pipeline extensions become simpler.

---

# ADR-005

## Title

Catalog-Driven Architecture

## Status

Accepted

## Version

v0.9.0

## Context

Hardcoded provider mappings would become increasingly difficult to maintain.

## Decision

The Catalog becomes the source of truth for:

- Canonical Types
- Attributes
- Capabilities
- Relationships

The Canonical Cloud Model executes the Catalog rather than embedding cloud knowledge in Python code.

---

# ADR-006

## Title

Traceability by Design

## Status

Accepted

## Version

v0.9.0

## Context

Compliance findings must be explainable.

Enterprise customers require evidence showing how findings were derived.

## Decision

Every CanonicalResource preserves a trace back to its originating ResolvedResource.

Future Evidence Engine and AI features consume this trace.

---

# ADR-007

## Title

Explainability over Convenience

## Status

Accepted

## Version

v0.9.0

## Decision

Every transformation performed by the Canonical Cloud Model must be explainable.

The platform should always be capable of answering:

- Why was this resource classified this way?
- Which attributes were normalized?
- Which capabilities were extracted?
- Why did this rule trigger?

---

# Future Decisions

The following topics require future architectural decisions.

Status: Open

- Multi-cloud normalization strategy
- Canonical capability taxonomy
- Security property model
- Risk scoring model
- Policy engine architecture
- AI integration
- Continuous compliance architecture