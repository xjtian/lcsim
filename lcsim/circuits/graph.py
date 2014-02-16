from collections import deque

import networkx as nx


def to_graph(circuit, weighted=True):
    """
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

    :type circuit Circuit
    :rtype networkx.Graph
    """
    result = nx.Graph()
    visited_gates = set()

    temp = set()
    for input_list in circuit._inputs:
        for (gate, _) in input_list:
            temp.add(gate)

    q = deque(temp)

    def bfs(to_visit):
        """
        Given an iterable of gates to visit, add them all to the graph as
        nodes.

        Returns a deque of all of the children of the given gates
        """
        neighbors = deque()
        while len(to_visit) > 0:
            gate = to_visit.popleft()

            visited_gates.add(gate)
            result.add_node(gate)

            neighbors.extend(gate.children)

        return neighbors

    # This adds all gates as nodes
    while len(q) > 0:
        q = bfs(q)

    #--------------------
    #--------------------
    # Now add all edges

    temp = set()
    for input_list in circuit._inputs:
        for (gate, _) in input_list:
            temp.add(gate)

    q = deque(temp)
    visited_gates = set()

    while len(q) > 0:
        gate = q.popleft()
        if gate in visited_gates:
            continue

        visited_gates.add(gate)
        for child in gate.children:
            if weighted:
                result.add_edge(gate, child, capacity=1)
            else:
                result.add_edge(gate, child)

            if child not in visited_gates:
                q.append(child)

    return result
