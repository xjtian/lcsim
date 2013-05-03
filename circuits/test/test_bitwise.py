__author__ = 'Jacky'

import unittest
import itertools

from circuits import bitwise, circuit
from components import sources


class TestBitwiseAnd(unittest.TestCase):
    def test_function(self):
        # Test all possible operations up to 8 bits
        for l in xrange(2, 9):

            space = [[0, 1] for _ in xrange(0, l)]
            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    c = bitwise.bitwise_and_circuit(l)
                    s = sources.DigitalArbitrary(x + y)

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)

                    source_c = circuit.Circuit('src', 0, 2 * l)
                    source_c.add_output_component(s, {i: i for i in
                                                      xrange(0, 2 * l)})
                    circuit.connect_circuits(source_c, c,
                                             {i: i for i in xrange(0, 2 * l)})

                    result = int(''.join(map(str, c.evaluate())), 2)
                    self.assertEqual(n1 & n2, result)


class TestBitwiseOr(unittest.TestCase):
    def test_function(self):
        # Test all possible operations up to 8 bits
        for l in xrange(2, 9):

            space = [[0, 1] for _ in xrange(0, l)]
            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    c = bitwise.bitwise_or_circuit(l)
                    s = sources.DigitalArbitrary(x + y)

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)

                    source_c = circuit.Circuit('src', 0, 2 * l)
                    source_c.add_output_component(s, {i: i for i in
                                                      xrange(0, 2 * l)})
                    circuit.connect_circuits(source_c, c,
                                             {i: i for i in xrange(0, 2 * l)})

                    result = int(''.join(map(str, c.evaluate())), 2)
                    self.assertEqual(n1 | n2, result)


class TestBitwiseXor(unittest.TestCase):
    def test_function(self):
        # Test all possible operations up to 8 bits
        for l in xrange(2, 9):

            space = [[0, 1] for _ in xrange(0, l)]
            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    c = bitwise.bitwise_xor_circuit(l)
                    s = sources.DigitalArbitrary(x + y)

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)

                    source_c = circuit.Circuit('src', 0, 2 * l)
                    source_c.add_output_component(s, {i: i for i in
                                                      xrange(0, 2 * l)})
                    circuit.connect_circuits(source_c, c,
                                             {i: i for i in xrange(0, 2 * l)})

                    result = int(''.join(map(str, c.evaluate())), 2)
                    self.assertEqual(n1 ^ n2, result)
