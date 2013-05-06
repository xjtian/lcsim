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


class TestRippleAdderNoCarry(unittest.TestCase):
    def test_function(self):
        # Test for all inputs up to 8 bits
        for l in xrange(2, 9):
            space = [[0, 1] for _ in xrange(0, l)]

            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)
                    mapping = {i: i for i in xrange(0, 2 * l)}

                    s = sources.DigitalArbitrary(x + y)
                    src = circuit.Circuit('src', 0, 2 * l)
                    src.add_output_component(s, mapping)

                    a = adders.ripple_adder_no_carry(l)
                    circuit.connect_circuits(src, a, mapping)

                    num = int(''.join(map(str, a.evaluate())), 2)
                    self.assertEqual('%dAdd' % l, a.name)
                    self.assertEqual((n1 + n2) % (2 ** l), num)
