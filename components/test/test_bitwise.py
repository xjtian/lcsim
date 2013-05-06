__author__ = 'Jacky'

import unittest
import itertools

from components import sources, bitwise


class TestBitwiseAND(unittest.TestCase):
    def test_constructor(self):
        a = bitwise.BitwiseAND(4)

        self.assertEqual('bAND', a.name)
        self.assertEqual(8, len(a._input_bits))
        self.assertEqual(4, len(a.output_bits))

    def test_evaluate(self):
        # Test for correctness for all inputs up to 8 bits
        for i in xrange(2, 9):
            a = bitwise.BitwiseAND(i)
            space = [[0, 1] for _ in xrange(0, i)]

            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    s = sources.DigitalArbitrary(x + y)

                    a.add_input(s, {j: j for j in xrange(0, 2 * i)})
                    a.evaluate()

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)
                    result = int(''.join(map(str, a.output_bits)), 2)
                    self.assertEqual(n1 & n2, result)

                    a.disconnect_inputs()


class TestBitwiseOR(unittest.TestCase):
    def test_constructor(self):
        a = bitwise.BitwiseOR(4)

        self.assertEqual('bOR', a.name)
        self.assertEqual(8, len(a._input_bits))
        self.assertEqual(4, len(a.output_bits))

    def test_evaluate(self):
        # Test for correctness for all inputs up to 8 bits
        for i in xrange(2, 9):
            a = bitwise.BitwiseOR(i)
            space = [[0, 1] for _ in xrange(0, i)]

            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    s = sources.DigitalArbitrary(x + y)

                    a.add_input(s, {j: j for j in xrange(0, 2 * i)})
                    a.evaluate()

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)
                    result = int(''.join(map(str, a.output_bits)), 2)
                    self.assertEqual(n1 | n2, result)

                    a.disconnect_inputs()


class TestBitwiseXOR(unittest.TestCase):
    def test_constructor(self):
        a = bitwise.BitwiseXOR(4)

        self.assertEqual('bXOR', a.name)
        self.assertEqual(8, len(a._input_bits))
        self.assertEqual(4, len(a.output_bits))

    def test_evaluate(self):
        # Test for correctness for all inputs up to 8 bits
        for i in xrange(2, 9):
            a = bitwise.BitwiseXOR(i)
            space = [[0, 1] for _ in xrange(0, i)]

            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    s = sources.DigitalArbitrary(x + y)

                    a.add_input(s, {j: j for j in xrange(0, 2 * i)})
                    a.evaluate()

                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)
                    result = int(''.join(map(str, a.output_bits)), 2)
                    self.assertEqual(n1 ^ n2, result)

                    a.disconnect_inputs()


class TestBitwiseNOT(unittest.TestCase):
    def test_constructor(self):
        a = bitwise.BitwiseNOT(4)

        self.assertEqual('bNOT', a.name)
        self.assertEqual(4, len(a._input_bits))
        self.assertEqual(4, len(a.output_bits))

    def test_evaluate(self):
        # Test for correctness for all inputs up to 8 bits
        for i in xrange(2, 9):
            a = bitwise.BitwiseNOT(i)
            space = [[0, 1] for _ in xrange(0, i)]

            it1 = itertools.product(*space)

            for x in it1:
                s = sources.DigitalArbitrary(x)

                a.add_input(s, {j: j for j in xrange(0, i)})
                a.evaluate()

                n1 = int(''.join(map(lambda x: '1' if x == 0 else '0', x)), 2)
                result = int(''.join(map(str, a.output_bits)), 2)
                self.assertEqual(n1, result)

                a.disconnect_inputs()
