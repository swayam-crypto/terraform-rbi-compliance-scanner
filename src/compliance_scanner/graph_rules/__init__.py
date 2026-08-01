"""
Graph-aware compliance rules.
"""

from .public_database_exposure import PublicDatabaseExposureRule

GRAPH_RULES = [
    PublicDatabaseExposureRule(),
]
