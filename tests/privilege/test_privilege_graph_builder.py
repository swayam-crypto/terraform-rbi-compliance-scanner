from compliance_scanner.engine.privilege.graph import (
    PrivilegeGraph,
)
from compliance_scanner.engine.privilege.graph_builder import (
    PrivilegeGraphBuilder,
)
from compliance_scanner.graph.resource_index import (
    ResourceIndex,
)


def test_builder_returns_graph():

    builder = PrivilegeGraphBuilder()

    graph = builder.build(
        ResourceIndex([]),
    )

    assert isinstance(
        graph,
        PrivilegeGraph,
    )


def test_builder_returns_empty_graph():

    builder = PrivilegeGraphBuilder()

    graph = builder.build(
        ResourceIndex([]),
    )

    assert (
        len(
            graph,
        )
        == 0
    )
