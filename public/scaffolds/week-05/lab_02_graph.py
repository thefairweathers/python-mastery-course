"""
Lab 5.2: Graph Traversal
========================

Implement graph operations using dicts (adjacency lists) and deque (BFS).
Practice choosing the right data structure for each operation.
"""

from collections import deque


def build_graph(edges: list[tuple[str, str]]) -> dict[str, set[str]]:
    """
    Build an undirected graph from a list of edges.

    Each edge is a tuple (node_a, node_b) meaning there's a connection
    between node_a and node_b in both directions.

    Return a dict mapping each node to a set of its neighbors.

    Example:
        build_graph([("A", "B"), ("B", "C")])
        → {"A": {"B"}, "B": {"A", "C"}, "C": {"B"}}
    """
    # TODO: Implement
    pass


def bfs(graph: dict[str, set[str]], start: str) -> list[str]:
    """
    Perform breadth-first search starting from 'start'.

    Return a list of nodes in the order they were visited.

    Hints:
    - Use a deque as your queue (append to add, popleft to remove)
    - Use a set to track visited nodes
    - Process neighbors in sorted order for deterministic results

    Example:
        graph = {"A": {"B", "C"}, "B": {"A"}, "C": {"A"}}
        bfs(graph, "A") → ["A", "B", "C"]
    """
    # TODO: Implement
    pass


def shortest_path(graph: dict[str, set[str]], start: str, end: str) -> list[str] | None:
    """
    Find the shortest path between two nodes using BFS.

    Return a list of nodes from start to end (inclusive), or None if
    no path exists.

    Hint: Track the parent of each node during BFS, then reconstruct
    the path by following parents from end back to start.

    Example:
        graph = build_graph([("A","B"), ("B","C"), ("A","D"), ("D","C")])
        shortest_path(graph, "A", "C") → ["A", "B", "C"] or ["A", "D", "C"]
    """
    # TODO: Implement
    pass


def connected_components(graph: dict[str, set[str]]) -> list[set[str]]:
    """
    Find all connected components in the graph.

    A connected component is a group of nodes where every node can
    reach every other node in the group.

    Return a list of sets, where each set contains the nodes in one
    connected component. Sort components by their smallest node.

    Example:
        graph = build_graph([("A","B"), ("C","D")])
        connected_components(graph) → [{"A", "B"}, {"C", "D"}]
    """
    # TODO: Implement
    pass


def has_cycle(graph: dict[str, set[str]]) -> bool:
    """
    Determine if the undirected graph contains a cycle.

    A cycle exists if during BFS/DFS, we encounter a visited node
    that is not the parent of the current node.

    Return True if a cycle exists, False otherwise.
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_build_graph():
    g = build_graph([("A", "B"), ("B", "C"), ("A", "C")])
    assert g["A"] == {"B", "C"}
    assert g["B"] == {"A", "C"}
    assert g["C"] == {"A", "B"}
    print("✓ build_graph passed")


def test_bfs():
    g = build_graph([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])
    result = bfs(g, "A")
    assert result[0] == "A"
    assert set(result) == {"A", "B", "C", "D"}
    print("✓ bfs passed")


def test_shortest_path():
    g = build_graph([("A", "B"), ("B", "C"), ("C", "D"), ("A", "D")])
    path = shortest_path(g, "A", "D")
    assert path is not None
    assert path[0] == "A" and path[-1] == "D"
    assert len(path) == 2, f"Expected direct path A→D, got {path}"

    assert shortest_path(g, "A", "Z") is None
    print("✓ shortest_path passed")


def test_connected_components():
    g = build_graph([("A", "B"), ("C", "D"), ("E", "F"), ("A", "E")])
    components = connected_components(g)
    assert len(components) == 2
    assert {"C", "D"} in components
    assert {"A", "B", "E", "F"} in components
    print("✓ connected_components passed")


def test_has_cycle():
    tree = build_graph([("A", "B"), ("A", "C"), ("B", "D")])
    assert has_cycle(tree) is False

    cyclic = build_graph([("A", "B"), ("B", "C"), ("C", "A")])
    assert has_cycle(cyclic) is True
    print("✓ has_cycle passed")


if __name__ == "__main__":
    test_build_graph()
    test_bfs()
    test_shortest_path()
    test_connected_components()
    test_has_cycle()
    print("\nAll tests passed! ✓")
