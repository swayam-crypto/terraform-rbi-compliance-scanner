# Canonical Resource

## Purpose

CanonicalResource represents cloud infrastructure semantically.

It is the output of the Canonical Cloud Model Pipeline.

Unlike ResolvedResource, CanonicalResource is independent of cloud providers and Infrastructure-as-Code formats.

---

# Relationship to ResolvedResource

ResolvedResource represents parsed infrastructure.

CanonicalResource represents normalized cloud infrastructure.

Pipeline

ResolvedResource

↓

Canonical Cloud Model Pipeline

↓

CanonicalResource

---

# Responsibilities

CanonicalResource should contain:

- Canonical Type
- Canonical Attributes
- Capabilities
- Security Properties
- Relationships
- Metadata
- Trace Information

It should not expose provider-specific implementation details unless explicitly preserved for traceability.

---

# Guiding Principle

Compliance rules should understand CanonicalResource.

They should never need to know whether infrastructure originated from Terraform, CloudFormation, Bicep, Pulumi, AWS, Azure, or Google Cloud.

---

# Traceability

Every CanonicalResource must preserve a reference to the original ResolvedResource.

This allows:

- Explainable findings
- Debugging
- Evidence generation
- Future remediation