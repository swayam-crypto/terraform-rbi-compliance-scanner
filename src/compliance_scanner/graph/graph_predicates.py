from compliance_scanner.graph.graph_query import GraphQuery
from compliance_scanner.models.resolved_resource import ResolvedResource


class GraphPredicates:
    """
    High-level business predicates for graph-aware compliance rules.

    Compliance rules should use this class instead of interacting with
    GraphQuery directly.
    """

    def __init__(
        self,
        query: GraphQuery,
    ):
        self.query = query

    def reachable_resources(
        self,
        resource: ResolvedResource,
    ) -> tuple[ResolvedResource, ...]:
        """
        Return every resource reachable from the given resource.
        """
        return self.query.reachable_resources(resource)

    def is_reachable(
        self,
        source: ResolvedResource,
        target: ResolvedResource,
    ) -> bool:
        """
        Return True if target is reachable from source.
        """
        return self.query.is_reachable(
            source,
            target,
        )

    def depends_on(
        self,
        resource: ResolvedResource,
        resource_type: str,
    ) -> bool:
        """
        Return True if the resource depends on at least one resource
        of the specified type.
        """
        return self.query.has_dependency(
            resource,
            resource_type,
        )

    def is_database(
        self,
        resource: ResolvedResource,
    ) -> bool:
        """
        Return True if the resource is a database.
        """

        return resource.resource_type in {
            "aws_db_instance",
            "aws_rds_cluster",
        }

    def is_public_entry_point(
        self,
        resource: ResolvedResource,
    ) -> bool:
        """
        Return True if the resource can act as a public entry point
        """

        return resource.resource_type in {
            "aws_lb",
            "aws_alb",
            "aws_api_gateway_rest_api",
            "aws_cloudfront_distribution",
        }
