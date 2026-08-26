from enum import StrEnum


class PrivilegeRelationshipType(StrEnum):
    """
    Canonical authorization relationships.

    These relationships model how identities, permissions and
    authorization objects are connected independently of any cloud
    provider.
    """

    IDENTITY = "identity"

    ASSUMES = "assumes"

    TRUSTS = "trusts"

    GRANTS = "grants"

    INHERITS = "inherits"

    MEMBER_OF = "member_of"

    BINDS = "binds"

    DELEGATES = "delegates"
