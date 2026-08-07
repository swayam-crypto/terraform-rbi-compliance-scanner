# Catalog Architecture

## Overview

The catalog is the knowledge base of the compliance scanner.

It provides a provider-independent representation of cloud resources so that
compliance rules do not need to understand provider-specific resource names.

Instead of writing rules against resources such as:

- aws_db_instance
- azurerm_postgresql_flexible_server
- google_sql_database_instance

the rule engine reasons about a single canonical concept:

Database

This allows the same compliance rule to work across multiple cloud providers
and Infrastructure-as-Code (IaC) frameworks.

---

# Goals

The catalog is designed to:

- Normalize provider-specific resources into canonical resource types.
- Describe compliance-relevant capabilities.
- Describe important relationships.
- Store metadata used by the compliance engine.
- Allow new cloud providers to be added without rewriting rules.

---

# High-Level Architecture

```
Terraform / CloudFormation / Pulumi / CDK / Bicep
                    │
                    ▼
             Resource Parser
                    │
                    ▼
            ResourceDefinition
                    │
                    ▼
          Compliance Catalog
                    │
                    ▼
        Graph + Rule Engine
                    │
                    ▼
         Compliance Findings
```

The catalog acts as the translation layer between provider-specific resources
and provider-independent compliance logic.

---

# ResourceDefinition

Every cloud resource is represented by a ResourceDefinition.

Example:

```yaml
aws_db_instance:
  provider: aws
  service: rds

  display_name: Amazon RDS DB Instance

  kind: data
  canonical_type: database

  capabilities:
    - encryption
    - backup
    - logging

  attributes:
    encryption:
      name: storage_encrypted
      type: boolean

  relationships:
    - subnet
    - security_group
    - kms_key

  aliases:
    - AWS::RDS::DBInstance
```

---

# Resource Identity

Every resource has two forms of identity.

## Provider

The cloud platform.

Examples

- aws
- azure
- gcp

---

## Service

The cloud service.

Examples

- rds
- s3
- ec2
- kms

---

# Resource Classification

## ResourceKind

ResourceKind describes the broad category of a resource.

Examples

- compute
- data
- network
- security
- storage
- identity

Rules rarely depend on ResourceKind directly.

It is mainly used for organization and reporting.

---

## CanonicalType

CanonicalType describes what the resource actually is.

Examples

- database
- object_storage
- load_balancer
- subnet
- security_group
- kms_key

Compliance rules should primarily reason using CanonicalType.

Example:

```
If a public entry point can reach a Database,
raise a finding.
```

Notice that the rule never references AWS.

---

# Capabilities

Capabilities describe what a resource can do.

Examples

- encryption
- logging
- backup
- public_entry_point

Capabilities represent behavior rather than identity.

For example

Database

is a CanonicalType.

Logging

is a capability.

---

# Attributes

Attributes describe compliance-relevant configuration.

Example

```yaml
attributes:

  encryption:
    name: storage_encrypted
    type: boolean

  backup_days:
    name: backup_retention_period
    type: integer
```

The compliance engine uses these mappings instead of hardcoding provider
attribute names inside rules.

---

# Relationships

Relationships describe connections between resources.

Example

```yaml
relationships:
  - subnet
  - security_group
  - kms_key
```

Relationships are consumed by the graph engine.

Example rule:

Public Load Balancer
        │
        ▼
Application
        │
        ▼
Database

↓

Public database exposure.

---

# Aliases

Aliases provide equivalent names used by different IaC frameworks.

Examples

Terraform

aws_db_instance

CloudFormation

AWS::RDS::DBInstance

Pulumi

aws:rds/instance:Instance

This allows the scanner to normalize multiple IaC frameworks into a single
catalog.

---

# Metadata

Metadata stores additional information that is not directly used by rules.

Example

```yaml
metadata:
  maturity: stable
  deprecated: false
```

Future versions may include

- documentation URLs
- supported compliance frameworks
- version information
- deprecation dates

---

# Catalog Loader

The CatalogLoader is responsible for

- Reading YAML files
- Validating resources
- Constructing ResourceDefinition objects
- Registering resources

Invalid catalog entries fail during loading rather than during scanning.

---

# Validation

Every resource is validated before loading.

Current validation includes

- Required fields
- ResourceKind validation
- CanonicalType validation
- Attribute validation
- Alias validation

This prevents malformed catalog entries from entering the compliance engine.

---

# Design Principles

The catalog follows several important principles.

## Provider Independence

Rules should never depend on AWS-specific resource names.

Instead of

aws_db_instance

use

CanonicalType.DATABASE

---

## Identity vs Behavior

Identity

- CanonicalType
- ResourceKind

Behavior

- Capabilities

This distinction keeps rules simple and reusable.

---

## Extensibility

Adding a new provider should require

1. Parsing resources.
2. Adding catalog entries.

Compliance rules should remain unchanged.

---

# Future Work

Planned improvements include

- AWS catalog expansion
- Azure support
- GCP support
- CloudFormation support
- Pulumi support
- Bicep support
- Capability enums
- Alias indexing
- Relationship validation
- Provider-specific metadata