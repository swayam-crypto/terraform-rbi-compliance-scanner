# Canonical Cloud Model (CCM)

## Purpose

The Canonical Cloud Model (CCM) is the semantic foundation of the Cloud Compliance Intelligence Platform (CCIP).

Its purpose is to transform provider-specific infrastructure into a provider-independent representation that can be understood by every component of the platform.

Rather than allowing compliance rules, reporting, graph analysis, or future AI capabilities to understand Terraform resources directly, every platform component consumes the Canonical Cloud Model.

---

# Why does it exist?

Cloud providers describe similar infrastructure using different resource types, attributes, and terminology.

Example:

AWS

aws_s3_bucket

Azure

azurerm_storage_account

Google Cloud

google_storage_bucket

Although they are implemented differently, they all represent the same cloud concept:

Object Storage.

The Canonical Cloud Model provides a single semantic representation for all cloud providers.

---

# Objectives

The Canonical Cloud Model should:

- Remove provider-specific logic from compliance rules.
- Support future multi-cloud expansion.
- Support future Infrastructure-as-Code expansion.
- Provide a stable semantic representation of cloud infrastructure.
- Enable explainable compliance decisions.
- Enable reusable compliance rules across providers.

---

# Current Architecture (v0.8.1)

Terraform

↓

Terraform Parser

↓

ResolvedResource

↓

Compliance Rules

↓

Reporting

---

# Target Architecture (v0.9)

Terraform

↓

Infrastructure Parser

↓

ResolvedResource

↓

Canonical Cloud Model Pipeline

↓

CanonicalResource

↓

Compliance Engine

↓

Evidence Engine

↓

Risk Engine

↓

Reporting

---

# Design Principles

The Canonical Cloud Model must remain:

- Cloud provider agnostic
- Infrastructure-as-Code agnostic
- Compliance framework agnostic
- Deterministic
- Explainable
- Extensible
- Testable
- Catalog-driven

---

# Responsibilities

The Canonical Cloud Model is responsible for:

- Semantic resource classification
- Attribute normalization
- Capability extraction
- Security property extraction
- Relationship normalization
- Trace generation

The Canonical Cloud Model is NOT responsible for:

- Parsing Infrastructure-as-Code
- Executing compliance rules
- Report generation
- Risk scoring
- Dashboard rendering

---

# Long-Term Vision

The Canonical Cloud Model becomes the single source of truth for cloud infrastructure inside CCIP.

Every future platform component should consume CanonicalResource rather than provider-specific infrastructure.