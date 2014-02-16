import sys

import random
import unittest

from lcsim.circuits.graph import to_graph
from lcsim.circuits import sources
from lcsim.sha1 import builder

from lcsim.components.base import ComponentBase


class TestToGraph(unittest.TestCase):
    def test_function(self):
        # DONT RUN THIS UNLESS YOU HAVE A LOT OF TIME, CPU, AND RAM TO BURN
        sys.setrecursionlimit(100000)

        message_circuit = sources.digital_source_int_circuit(random.getrandbits(512), 512)
        _, h = builder.sha1(message_circuit)

        # g = to_graph(message_circuit._outputs)
        # print len(g.nodes())
        # print len(g.edges())

        print ComponentBase.count
