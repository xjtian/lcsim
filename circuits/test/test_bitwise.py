__author__ = 'Jacky'

import unittest
import itertools

from circuits import bitwise, circuit, sources


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

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)

                    source_c = sources.digital_source_circuit(x + y)
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

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)

                    source_c = sources.digital_source_circuit(x + y)

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

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)

                    source_c = sources.digital_source_circuit(x + y)
                    circuit.connect_circuits(source_c, c,
                                             {i: i for i in xrange(0, 2 * l)})

                    result = int(''.join(map(str, c.evaluate())), 2)
                    self.assertEqual(n1 ^ n2, result)


class TestBitwiseNot(unittest.TestCase):
    def test_function(self):
        # Test all possible operations up to 8 bits
        for l in xrange(2, 9):
            space = [[0, 1] for _ in xrange(0, l)]
            it1 = itertools.product(*space)

            for x in it1:
                c = bitwise.bitwise_not_circuit(l)

                n = int(''.join(map(lambda y: '0' if y else '1', x)), 2)

                source_c = sources.digital_source_circuit(x)
                circuit.connect_circuits(source_c, c,
                                         {i: i for i in xrange(0, l)})

                result = int(''.join(map(str, c.evaluate())), 2)
                self.assertEqual(n, result)
