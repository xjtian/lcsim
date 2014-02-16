import unittest

from lcsim.circuits.graph import to_graph
from lcsim.circuits import adders


class TestToGraph(unittest.TestCase):
    def test_function(self):
        full_adder = adders.full_adder_circuit()

        g = to_graph(full_adder)

        print g.nodes()
        print g.edges()
