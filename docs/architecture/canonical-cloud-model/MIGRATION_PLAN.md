# Canonical Cloud Model Migration Plan

## Goal

Migrate CCIP from provider-specific compliance evaluation to semantic cloud compliance evaluation.

---

# Current State

Terraform

↓

ResolvedResource

↓

Compliance Rules

---

# Target State

Terraform

↓

ResolvedResource

↓

Canonical Cloud Model Pipeline

↓

CanonicalResource

↓

Compliance Rules

---

# Milestones

## Phase 1

Canonical Cloud Model Architecture

Status

⬜ Planned

---

## Phase 2

CanonicalResource

Status

⬜ Planned

---

## Phase 3

Canonical Cloud Model Pipeline

Status

⬜ Planned

---

## Phase 4

Rule Migration

Status

⬜ Planned

---

## Phase 5

Regression Testing

Status

⬜ Planned

---

## Phase 6

Release v0.9.0

Status

⬜ Planned

---

# Backward Compatibility

During migration:

- ResolvedResource remains supported.
- Existing Terraform parsing remains unchanged.
- Existing compliance findings should remain functionally equivalent.
- Rule behavior should not regress.

---

# Success Criteria

v0.9.0 is complete when:

- Compliance rules operate on CanonicalResource.
- Terraform behavior remains unchanged.
- The architecture supports future cloud providers without modifying compliance rules.