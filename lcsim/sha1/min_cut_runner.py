import sys
import random

import networkx as nx

from lcsim.sha1.graph import to_graph
from lcsim.circuits import circuit, sources
from lcsim.sha1 import builder
from lcsim.components.base import ComponentBase


def main():
    sys.setrecursionlimit(100000)

    a = sources.digital_source_int_circuit(0x67452301, 32)
    b = sources.digital_source_int_circuit(0xEFCDAB89, 32)
    c = sources.digital_source_int_circuit(0x98BADCFE, 32)
    d = sources.digital_source_int_circuit(0x10325476, 32)
    e = sources.digital_source_int_circuit(0xC3D2E1F0, 32)

    message_circuit = sources.digital_source_int_circuit(random.getrandbits(512), 512)

    h0, h1, h2, h3, h4 = builder.block_operation(message_circuit, a, b, c, d, e)

    # Concatenate results
    h01 = circuit.stack_circuits('h01', h0, h1)
    h012 = circuit.stack_circuits('h012', h01, h2)
    h0123 = circuit.stack_circuits('h0123', h012, h3)

    h = circuit.stack_circuits('H', h0123, h4)

    g = to_graph(message_circuit._outputs)

    # All gates/nodes that input hooks into
    # a = set()
    # for gate in message_circuit._outputs:
    #     a |= set(g.neighbors(gate))
    #     g.remove_node(gate)
    #
    # g.add_node('source')
    # for gate in a:
    #     g.add_edge('source', gate)
    #
    # g.add_node('sink')
    # for gate in h._outputs:
    #     g.add_edge(gate, 'sink')

    g.add_node('source')
    for gate in message_circuit._outputs:
        g.add_edge('source', gate, capacity=1)

    g.add_node('sink')
    for gate in h._outputs:
        g.add_edge(gate, 'sink', capacity=1)

    print 'Number of nodes in circuit graph: %d' % len(g.nodes())
    print 'Number of edges in circuit graph: %d' % len(g.edges())
    print 'Total number of instantiated components: %d' % ComponentBase.count

    mc = nx.max_flow(g, 'source', 'sink')

    print 'Min-cut size: %d' % mc


if __name__ == '__main__':
    main()
