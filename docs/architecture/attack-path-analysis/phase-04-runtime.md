# Attack Path Analysis

## Goal

Introduce a provider-independent attack path analysis engine capable of discovering exploitable paths through infrastructure resources using the existing graph runtime, canonical cloud model, and capability system.

---
# Phase 4 - Runtime Audit

---

## Files

- scan_context.py
- core/scan_engine.py
- core/terraform_scan.py
- cli.py

---

# Runtime Architecture

Current execution pipeline

Terraform

↓

TerraformParser

↓

ResolvedResource

↓

RelationshipResolver

↓

RelationshipGraph

↓

Graph Rules

↓

Findings

The runtime is already layered correctly.

No parser knows about graph rules.

No graph knows about compliance.

No compliance rule knows about parsing.

Excellent separation.

---

## File

scan_context.py

### Responsibility

Shared runtime state passed into every graph-aware component.

Current contents

- resources
- resource_index
- relationship_graph

### Strengths

Very lightweight.

Acts as the runtime contract.

Graph rules receive everything they need.

### Weaknesses

Attack Path Analysis will produce a reusable analysis result.

There is currently nowhere to store it.

Example

AttackPathEngine

↓

AttackPathCollection

↓

GraphRule A

↓

GraphRule B

↓

GraphRule C

Without ScanContext support every rule would recompute attack paths.

### Attack Path Impact

Eventually ScanContext should contain:

attack_paths

However...

NOT during the first implementation.

The first version should prove the API before modifying ScanContext.

### Decision

No runtime changes during Attack Path Analysis v1.

---

## File

core/scan_engine.py

### Responsibility

Coordinates the complete scan lifecycle.

Current stages

1. Resource rules

↓

2. Relationship resolution

↓

3. Graph construction

↓

4. Graph rules

### Strengths

Pipeline is very clear.

Every stage has one responsibility.

Excellent orchestration.

### Weaknesses

No analysis stage exists.

Today:

Graph

↓

Rules

Future:

Graph

↓

Attack Analysis

↓

Rules

This is the only architectural gap discovered so far.

### Attack Path Impact

Eventually the runtime will become

Resources

↓

Relationship Resolution

↓

Relationship Graph

↓

Attack Path Engine

↓

Graph Rules

The attack engine should execute exactly once.

Attack-path-aware graph rules should consume attack path analysis.

Relationship-based graph rules should continue using GraphQuery.

### Decision

No changes during Phase 1.

AttackPathEngine should initially be invoked manually by tests until its API stabilizes.

Only then should ScanEngine integrate it.

---

## File

core/terraform_scan.py

### Responsibility

Terraform adapter.

Owns:

- parsing
- suppressions
- caching
- streaming scan

### Strengths

Entirely Terraform specific.

No graph logic.

No compliance logic.

No attack logic.

Exactly the separation we wanted.

### Weaknesses

None relevant.

Attack analysis should never appear here.

### Attack Path Impact

No changes required.

---

## File

cli.py

### Responsibility

Application entry point.

Owns:

- arguments
- reporting
- exit codes

### Strengths

Very small.

No business logic.

Correct separation.

### Weaknesses

None.

### Attack Path Impact

No changes required.

Attack Path Analysis should remain an internal runtime capability.

CLI should not know whether findings came from graph traversal or attack path analysis.

---

# Runtime Decision

Current runtime architecture is approved.

The only future addition is:

RelationshipGraph

↓

AttackPathEngine

↓

AttackPathCollection

↓

Graph Rules

This should become a new runtime stage.

It should execute once per scan.

The CLI, Terraform adapter and parser remain completely unchanged.