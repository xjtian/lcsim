__author__ = 'Jacky'

import unittest
from components import sources


class TestDigitalZero(unittest.TestCase):
    """
    Test for DigitalZero class.
    """
    def setUp(self):
        self.gate = sources.DigitalZero()

    def test_constructor(self):
        self.assertEqual('D0', self.gate.name)
        self.assertEqual(0, len(self.gate._input_bits))
        self.assertEqual(1, len(self.gate.output_bits))
        self.assertEqual([0], self.gate.output_bits)

    def test_evaluate(self):
        self.gate.evaluate()
        self.assertEqual([0], self.gate.output_bits)


class TestDigitalOne(unittest.TestCase):
    """
    Test for DigitalOne class.
    """
    def setUp(self):
        self.gate = sources.DigitalOne()

    def test_constructor(self):
        self.assertEqual('D1', self.gate.name)
        self.assertEqual(0, len(self.gate._input_bits))
        self.assertEqual(1, len(self.gate.output_bits))
        self.assertEqual([1], self.gate.output_bits)

    def test_evaluate(self):
        self.gate.evaluate()
        self.assertEqual([1], self.gate.output_bits)
