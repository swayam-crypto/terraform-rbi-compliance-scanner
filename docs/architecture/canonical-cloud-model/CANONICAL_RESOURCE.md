# Responsibility

`CanonicalResource` is the canonical, provider-independent representation of a cloud resource within CCIP.

It represents **what a cloud resource is**, rather than **how it is implemented** by a specific cloud provider or Infrastructure-as-Code language.

`CanonicalResource` is the primary data model consumed by the Compliance Engine and future platform components, including the Evidence Engine, Risk Engine, Graph Engine, Reporting, Dashboard, and AI capabilities.

Its purpose is to provide a stable semantic representation of cloud infrastructure that remains consistent regardless of:

- Cloud provider (AWS, Azure, Google Cloud, OCI, etc.)
- Infrastructure-as-Code language (Terraform, OpenTofu, CloudFormation, Bicep, Pulumi, Kubernetes, etc.)
- Compliance framework (RBI, DPDP, CIS, ISO 27001, NIST, SOC 2, etc.)

---

## Responsibilities

`CanonicalResource` is responsible for representing:

- The canonical identity of a cloud resource.
- The canonical resource type.
- Canonical attributes.
- Resource capabilities.
- Security properties.
- Canonical relationships to other resources.
- Metadata required for compliance evaluation.
- Traceability back to the originating infrastructure definition.

---

## CanonicalResource Contract

The Canonical Cloud Model Pipeline constructs `CanonicalResource` by combining information from three sources:

| CanonicalResource Field | Source | Purpose |
|--------------------------|--------|---------|
| Platform | ResolvedResource | Preserve Infrastructure-as-Code origin |
| Provider | ResolvedResource | Preserve cloud provider |
| Canonical Type | Catalog | Semantic classification |
| Canonical Attributes | Canonical Cloud Model Pipeline | Provider-independent representation |
| Capabilities | Catalog | Resource capability model |
| Security Properties | Canonical Cloud Model Pipeline | Compliance evaluation |
| Relationships | Canonical Cloud Model Pipeline | Semantic graph representation |
| Metadata | Catalog | Resource metadata |
| Trace | ResolvedResource + Pipeline | Explainability and debugging |

Each field must have a single owner.

The Canonical Cloud Model Pipeline must never duplicate or redefine information that already exists within the Catalog or the original ResolvedResource.

---

## Non-Responsibilities

`CanonicalResource` is **not** responsible for:

- Parsing Infrastructure-as-Code.
- Normalizing infrastructure.
- Executing compliance rules.
- Graph construction or traversal.
- Risk scoring.
- Report generation.
- Evidence generation.
- Dashboard presentation.
- Infrastructure modification or remediation.

Those responsibilities belong to other components of the platform.

---

## Design Principles

`CanonicalResource` should be:

- Immutable after creation.
- Provider-independent.
- Infrastructure-as-Code independent.
- Compliance framework independent.
- Deterministic.
- Explainable.
- Serializable.
- Backward compatible where practical.

---

## Relationship with ResolvedResource

`ResolvedResource` represents parsed infrastructure.

`CanonicalResource` represents semantic cloud infrastructure.

The Canonical Cloud Model Pipeline transforms:

ResolvedResource

↓

CanonicalResource

without modifying the original `ResolvedResource`.

This separation preserves parser fidelity while providing a stable semantic model for the rest of the platform.

---

## Guiding Principle

`CanonicalResource` is the single semantic representation of cloud infrastructure inside CCIP.

Every platform component beyond the parsing layer should consume `CanonicalResource` instead of provider-specific infrastructure models.

---

## Ownership Model

The Canonical Cloud Model follows a strict ownership model.

Infrastructure Parser owns:

- ResolvedResource

Catalog owns:

- Canonical Types
- Resource Definitions
- Capabilities
- Metadata

Canonical Cloud Model Pipeline owns:

- CanonicalResource construction
- Canonical attribute mapping
- Security property extraction
- Relationship normalization
- Trace generation

Compliance Engine owns:

- Rule evaluation
- Findings

Reporting owns:

- Report generation

No component should modify objects owned by another component.

---

## Future Extensions

The CanonicalResource model is intentionally minimal.

Future platform components may consume CanonicalResource to implement:

- Evidence Engine
- Risk Engine
- Policy Engine
- Relationship Intelligence
- AI Assistant
- Dashboard
- REST API

These components extend the platform without changing the CanonicalResource contract.