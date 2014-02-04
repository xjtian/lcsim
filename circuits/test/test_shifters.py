__author__ = 'Jacky'

import unittest
import itertools

from circuits import shifters, circuit
from components import sources


class TestLeftRotate(unittest.TestCase):
    def test_function(self):
        # Test all possible inputs up to 4 bits.
        for size in xrange(2, 5):
            space = [[0, 1] for _ in xrange(0, size)]

            for output in itertools.product(*space):
                for shift in xrange(0, 2 * size):
                    c = circuit.Circuit('', 0, size)
                    s = sources.DigitalArbitrary(output)

                    c.add_output_component(s, {i: i for i in xrange(0, size)})

                    # It's the same algorithm as the code being tested...
                    shifted = output[shift % size:] + output[:shift % size]
                    shifted = list(shifted)

                    # Also make sure it's in place
                    self.assertIs(c, shifters.left_rotate_in_place(c, shift))
                    self.assertEqual(shifted, c.evaluate())


class TestRightRotate(unittest.TestCase):
    def test_function(self):
        # Test all possible inputs up to 4 bits.
        for size in xrange(2, 5):
            space = [[0, 1] for _ in xrange(0, size)]

            for output in itertools.product(*space):
                for shift in xrange(0, 2 * size):
                    c = circuit.Circuit('', 0, size)
                    s = sources.DigitalArbitrary(output)

                    c.add_output_component(s, {i: i for i in xrange(0, size)})

                    # It's the same algorithm as the code being tested...
                    i = size - (shift % size)
                    shifted = output[i:] + output[:i]
                    shifted = list(shifted)

                    # Also make sure it's in place
                    self.assertIs(c, shifters.right_rotate(c, shift))
                    self.assertEqual(shifted, c.evaluate())
