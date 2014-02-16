import sys

import random
import unittest

import networkx as nx

from lcsim.circuits.graph import to_graph
from lcsim.circuits import sources
from lcsim.sha1 import builder

from lcsim.components.base import ComponentBase


class TestToGraph(unittest.TestCase):
    def test_function(self):
        sys.setrecursionlimit(100000)

        message_circuit = sources.digital_source_int_circuit(random.getrandbits(512), 512)
        _, h = builder.sha1(message_circuit)

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

        print 'Min-cut size: %d' % nx.max_flow(g, 'source', 'sink')
