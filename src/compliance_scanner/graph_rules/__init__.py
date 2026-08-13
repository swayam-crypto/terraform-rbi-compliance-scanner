"""Experimental graph-rule package.

``GRAPH_RULES`` is intentionally future-only and is not executed by production
scans. Production execution is owned exclusively by
``compliance_scanner.rules.registry.GRAPH_RULES``. Keep this package for
isolated rule development and tests until a later, explicitly approved rule
pack consolidation.
"""

from .public_database_exposure import PublicDatabaseExposureRule

GRAPH_RULES = [
    # Experimental/future-only: do not add this collection to production scans.
    PublicDatabaseExposureRule(),
]
