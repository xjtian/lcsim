__author__ = 'Jacky'

import unittest
import itertools

from circuits import circuit, adders
from components import sources


class TestFullAdder(unittest.TestCase):
    def test_function(self):
        # Test for all inputs
        it = itertools.product([0, 1], [0, 1], [0, 1])

        for x in it:
            s = sources.DigitalArbitrary(x)
            src = circuit.Circuit('src', 0, 3)
            src.add_output_component(s, {0: 0, 1: 1, 2: 2})

            a = adders.full_adder_circuit()
            circuit.connect_circuits(src, a, {0: 0, 1: 1, 2: 2})

            num = int(''.join(map(str, a.evaluate())), 2)
            self.assertEqual(sum(x), num)
