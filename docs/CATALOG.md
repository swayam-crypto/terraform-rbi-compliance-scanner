# Catalog Architecture

## Purpose

The catalog is CCIP's stable knowledge layer. It translates a
provider-specific resource identifier and configuration into concepts that
rules, graph analysis, reporting, and future IaC parsers can share.

The catalog does not parse Terraform, make compliance findings, or build a
graph. It defines the metadata that lets those components use a common
vocabulary.

```text
Terraform / CloudFormation / Pulumi / Bicep / Kubernetes
                         |
                         v
                  ResolvedResource
                         |
                         v
                   Compliance Catalog
                         |
                         +--> Rules
                         +--> Relationship extraction
                         +--> Reporting
```

## Resource definitions

Each catalog entry becomes an immutable `ResourceDefinition`. A definition
contains provider and service identity, a canonical classification,
capabilities, canonical attribute mappings, aliases, relationships, and
extensible metadata.

```yaml
aws_db_instance:
  provider: aws
  service: rds
  display_name: Amazon RDS DB Instance

  kind: data
  canonical_type: database

  capabilities:
    - data_store
    - encryption_at_rest
    - backup

  attributes:
    encryption:
      name: storage_encrypted
      type: boolean
```

The YAML files are loaded by `CatalogLoader`, validated, and registered in an
immutable catalog model. Consumers should use `Catalog` rather than reaching
into the registry directly.

## Canonical types

A canonical type identifies what a resource *is*, independently of the IaC
syntax or cloud-provider-specific resource name. Canonical types exist so a
rule can reason about a `database`, `object_storage`, `load_balancer`,
`security_group`, or `kms_key` without first branching on Terraform resource
names.

Examples:

| Provider-specific resource | Canonical type |
|---|---|
| `aws_db_instance` | `database` |
| `aws_s3_bucket` | `object_storage` |
| `aws_lb` | `load_balancer` |
| `aws_security_group` | `security_group` |
| `aws_kms_key` | `kms_key` |

Canonical types are intentionally a controlled vocabulary defined by
`CanonicalType`. A catalog entry may use the closest available canonical type
while the vocabulary evolves. That is preferable to embedding provider names
in rules or creating ad-hoc types per provider.

`ResourceKind` is a broader organizational classification such as `compute`,
`storage`, `data`, `network`, or `identity`. It complements, rather than
replaces, the more specific canonical type.

## Capabilities

A capability describes a relevant property, behavior, or control surface of a
resource. Rules use capabilities to determine whether a resource is eligible
for a control without hardcoding provider resource names.

Examples of behavioral capabilities:

- `encryption_at_rest`
- `data_residency`
- `backup`
- `audit_logging`
- `public_entry_point`
- `private_networking`

Some capabilities are identity-adjacent. Examples include `block_storage`,
`file_storage`, `message_queue`, `subnet`, and `network_interface`. These are
retained because they express the capability boundary needed by current rules
and may be more precise than a broad canonical type in a specific policy.

Capabilities are not currently an enum. Their names are intentionally
preserved as stable catalog vocabulary: renaming them would affect rules,
controls, and future provider mappings. Similar-looking names can represent
different concepts; for example, `logging`, `audit_logging`, and
`access_logging` have distinct policy meanings. New entries should follow the
existing vocabulary and document their intended distinction rather than
renaming existing values opportunistically.

## Attributes

Attribute keys in the catalog are canonical names; `name` identifies the
provider-specific field on `ResolvedResource.attributes`.

```yaml
attributes:
  encryption:
    name: storage_encrypted
    type: boolean
```

In this example, rules ask for the canonical `encryption` attribute while the
catalog resolves it to AWS's `storage_encrypted`. This separation is central to
multi-cloud and multi-IaC normalization.

## Aliases

Aliases record equivalent identifiers for the same conceptual resource across
IaC ecosystems and provider representations. For example, an AWS resource may
have Terraform, CloudFormation, and Pulumi identifiers:

```yaml
aliases:
  - AWS::RDS::DBInstance
  - aws:rds/instance:Instance
```

Aliases support future source-format and provider mapping without requiring a
rule to know every source spelling. They do not by themselves establish that
two different cloud providers are interchangeable; that normalization happens
through shared canonical types, capabilities, and attributes.

Some resources intentionally have no aliases yet. An empty alias list means
that an authoritative equivalent identifier has not been added, not that the
resource is unsupported or less valid. Alias coverage should grow from verified
provider/IaC documentation, not inferred naming conventions.

## Metadata

`metadata` carries extensible information that is not necessarily consumed by
the current rule engine. Existing entries commonly use:

```yaml
metadata:
  maturity: stable
  deprecated: false
```

- `maturity` communicates catalog confidence or lifecycle status.
- `deprecated` reserves a clear migration signal for entries that should no
  longer be selected by future normalization or catalog tooling.

Metadata is deliberately preserved even when no current runtime component
reads it. Future uses may include documentation URLs, source/provider versions,
framework coverage, deprecation dates, compatibility notes, and catalog
quality signals. Missing metadata on an entry is not an instruction to remove
metadata from other entries.

## Relationships

The catalog and graph layers use three related but distinct concepts.

| Concept | Owner | Meaning | Current behavior |
|---|---|---|---|
| `ResourceDefinition.relationships` | Resource-level catalog YAML | A descriptive set of relationship categories known to be relevant for this resource. | Descriptive metadata today; it is not directly used by extraction. |
| `AttributeDefinition.relationship` | An individual catalog attribute | Executable extraction metadata: relationship type, required flag, and expected target canonical type. | Consumed by `RelationshipResolver`. |
| `Relationship` | Graph runtime model | A concrete directed edge from one resolved resource to another. | Added to `RelationshipGraph` for traversal and graph rules. |

### Resource-level relationship metadata

```yaml
relationships:
  - subnet
  - security_group
  - kms_key
```

`ResourceDefinition.relationships` describes the relationships a resource is
expected or known to participate in. It is valuable catalog knowledge for
future validation, coverage reporting, user interfaces, and additional
extraction strategies. It is currently descriptive metadata and does not, by
itself, create graph edges.

### Executable attribute relationship metadata

```yaml
attributes:
  subnet_id:
    name: subnet_id
    type: string
    relationship:
      type: subnet
      target: subnet
      required: false
```

`AttributeDefinition.relationship` instructs the current extractor how to
interpret a provider attribute. It identifies the canonical relationship type
and the expected target canonical type. This is the only relationship metadata
used by the current extraction algorithm.

### Relationship extraction flow

```text
Catalog YAML
     |
     v
CatalogLoader
     |
     v
AttributeDefinition.relationship
(RelationshipDefinition)
     |
     v
RelationshipResolver
     |
     v
Relationship
     |
     v
RelationshipGraph
```

At runtime, `RelationshipResolver` iterates catalog attributes that have an
`AttributeDefinition.relationship`, reads the corresponding resource value,
parses supported Terraform-style references, resolves a target through
`ResourceIndex`, and confirms that the target's canonical type matches the
definition. Each successful match becomes a runtime `Relationship` edge.

## Validation

`CatalogLoader` currently validates:

- required identity and classification fields;
- known `ResourceKind` and `CanonicalType` values;
- attribute names and attribute types;
- duplicate physical attribute names within one resource;
- duplicate aliases within one resource.

The catalog is intentionally extensible. Metadata, aliases, capabilities, and
descriptive relationships should not be removed merely because a current
runtime consumer does not use every field.

## Adding catalog entries

When adding an entry:

1. Use a provider-specific resource identifier as the YAML key.
2. Choose the closest existing canonical type and resource kind.
3. Add capabilities using the established vocabulary.
4. Map compliance-relevant provider fields to canonical attribute keys.
5. Add `AttributeDefinition.relationship` only when the field is an executable
   relationship reference for the current extractor.
6. Preserve descriptive resource-level relationship metadata where it improves
   catalog knowledge, even if it is not executable today.
7. Add aliases only when they are authoritative.
8. Include metadata where its lifecycle or maturity information is known.

The catalog should grow through deliberate, compatible additions. It is the
stable foundation for future normalization, not a cache of only today's rule
lookups.
