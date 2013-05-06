__author__ = 'Jacky'

import unittest
import itertools

from components import adders, sources


class TestHalfAdder(unittest.TestCase):
    def test_constructor(self):
        a = adders.HalfAdder()

        self.assertEqual('HAdd', a.name)
        self.assertEqual(2, len(a._input_bits))
        self.assertEqual(2, len(a.output_bits))

    def test_evaluate(self):
        a = adders.HalfAdder()

        for i in [0, 1]:
            for j in [0, 1]:
                s = sources.DigitalArbitrary([i, j])

                a.add_input(s, {0: 0, 1: 1})
                a.evaluate()

                result = int(''.join(map(str, a.output_bits)), 2)
                self.assertEqual(i + j, result)

                a.disconnect_inputs()


class TestFullAdder(unittest.TestCase):
    def test_constructor(self):
        a = adders.FullAdder()

        self.assertEqual('FAdd', a.name)
        self.assertEqual(3, len(a._input_bits))
        self.assertEqual(2, len(a.output_bits))

    def test_evaluate(self):
        a = adders.FullAdder()

        for i in [0, 1]:
            for j in [0, 1]:
                for k in [0, 1]:
                    s = sources.DigitalArbitrary([i, j, k])

                    a.add_input(s, {0: 0, 1: 1, 2: 2})
                    a.evaluate()

                    result = int(''.join(map(str, a.output_bits)), 2)
                    self.assertEqual(i + j + k, result)

                    a.disconnect_inputs()


class TestNBitAdder(unittest.TestCase):
    def test_constructor(self):
        a = adders.NBitAdder(2)

        self.assertEqual('2Add', a.name)
        self.assertEqual(4, len(a._input_bits))
        self.assertEqual(3, len(a.output_bits))

    def test_evaluate(self):
        # Test all possible additions up to 8 bits
        for i in xrange(2, 9):
            a = adders.NBitAdder(i)
            space = [[0, 1] for _ in xrange(0, i)]

            iter1 = itertools.product(*space)
            iter2 = itertools.product(*space)

            for x in iter1:
                for y in iter2:
                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)
                    s = sources.DigitalArbitrary(x + y)

                    a.add_input(s, {i: i for i in xrange(0, len(x + y))})
                    a.evaluate()

                    result = int(''.join(map(str, a.output_bits)), 2)
                    self.assertEqual(n1 + n2, result)

                    a.disconnect_inputs()
