from dataclasses import dataclass

from compliance_scanner.models.resolved_resource import ResolvedResource


@dataclass(
    frozen=True,
    slots=True,
)
class EffectivePermission:
    """
    Represents an effective permission granted to a resource.

    The permission itself is cloud-agnostic. The resource that granted
    the permission is preserved so higher analysis layers can explain
    why the permission exists.
    """

    name: str

    granted_by: ResolvedResource


@dataclass(
    frozen=True,
    slots=True,
)
class EffectiveIdentity:
    """
    Represents the effective identity of a resource.

    Identity analysis computes the authorization context of a resource,
    including the identities attached to it and the permissions those
    identities ultimately provide.

    The model intentionally avoids cloud-specific concepts such as
    IAM Roles, Managed Identities or Service Accounts.
    """

    resource: ResolvedResource

    identities: tuple[ResolvedResource, ...]

    identity_chain: tuple[ResolvedResource, ...]

    permissions: tuple[EffectivePermission, ...]
