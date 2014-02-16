from collections import deque

import networkx as nx


def to_graph(inputs, weighted=True):
    """
    TODO: update this docstring

    Run a BFS on a given circuit and return a networkx graph of the
    graph representation of the circuit with gates as nodes and connections
    between gates as edges.

    Parameters:
        circuit:
            The Circuit object to turn into a graph.
        weighted:
            If True, each edge in the graph will have capacity 1, otherwise
            the graph will be unweighted.

    Returns:
        A networkx graph of the circuit.

    :type circuit list[ComponentBase]
    :rtype networkx.Graph
    """
    result = nx.Graph()
    # processed contains all gates that have been added to the graph as a
    # node AND is connected to all neighbors in the graph
    processed = set()
    q = deque(set(inputs))

    while len(q) > 0:
        gate = q.popleft()
        if gate not in result:
            result.add_node(gate)

        for child in gate.children:
            if child not in result:
                result.add_node(child)

            if child not in processed:
                q.append(child)

            if weighted:
                result.add_edge(gate, child, capacity=1)
            else:
                result.add_edge(gate, child)

        for parent in gate.parents:
            if parent not in result:
                result.add_node(parent)

            if parent not in processed:
                q.append(parent)

            if weighted:
                result.add_edge(parent, gate, capacity=1)
            else:
                result.add_edge(parent, gate)

        processed.add(gate)

    return result
