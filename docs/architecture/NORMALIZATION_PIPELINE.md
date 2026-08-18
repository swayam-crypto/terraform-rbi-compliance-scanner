# Canonical Cloud Model Pipeline

## Purpose

The Canonical Cloud Model Pipeline transforms provider-specific infrastructure into CanonicalResource.

Each stage performs one well-defined transformation.

---

# Pipeline

ResolvedResource

↓

Resource Classification

↓

Canonical Type Mapping

↓

Attribute Normalization

↓

Capability Extraction

↓

Security Property Extraction

↓

Relationship Normalization

↓

Trace Generation

↓

CanonicalResource

---

# Stage Responsibilities

## Resource Classification

Determine the semantic cloud concept.

Example

aws_s3_bucket

↓

Object Storage

---

## Attribute Normalization

Map provider-specific attributes into canonical attributes.

---

## Capability Extraction

Determine which capabilities the resource provides.

Examples

Encryption

Logging

Versioning

Private Networking

---

## Security Property Extraction

Produce compliance-ready security properties.

Examples

Encrypted

Public

Versioning Enabled

Logging Enabled

---

## Relationship Normalization

Convert infrastructure relationships into canonical graph relationships.

---

## Trace Generation

Record every transformation performed by the pipeline.

This provides explainability for future reporting and AI capabilities.

---

# Principles

Every pipeline stage should:

- Have one responsibility.
- Be independently testable.
- Produce deterministic output.
- Never modify previous stages.