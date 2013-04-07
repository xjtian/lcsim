__author__ = 'Jacky'

import unittest
from components import sources


class TestDigitalSourceBase(unittest.TestCase):
    """
    Test for DigitalSourceBase class.
    """
    def test_constructor(self):
        gate = sources.DigitalSourceBase('Test', [0, 1, 1])

        self.assertEqual('Test', gate.name)
        self.assertEqual([0, 1, 1], gate.output_bits)
        self.assertEqual(0, len(gate._input_bits))

        # Make sure exception is raised if non-bit value is passed
        try:
            sources.DigitalSourceBase('Test', [1, 0, 1, 2])
            self.fail('Digital source allowed non-bit value')
        except ValueError:
            self.assert_(True)

    def test_evaluate(self):
        gate = sources.DigitalSourceBase('Test', [0, 1, 1, 0, 1, 1])
        # Arbitrarily modify output_bits to make sure it goes back to what it should be
        gate.output_bits = [1, 2, 3]
        gate.evaluate()
        self.assertEqual([0, 1, 1, 0, 1, 1], gate.output_bits)


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
        self.gate.output_bits = [2]
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
        self.gate.output_bits = [2]
        self.gate.evaluate()
        self.assertEqual([1], self.gate.output_bits)


class TestDigitalArbitrary(unittest.TestCase):
    """
    Test for DigitalArbitrary class.
    """
    def setUp(self):
        self.output = [0, 1, 1, 0]
        self.gate = sources.DigitalArbitrary(self.output)

    def test_constructor(self):
        self.assertEqual('DArb', self.gate.name)
        self.assertEqual(0, len(self.gate._input_bits))
        self.assertEqual(len(self.output), len(self.gate.output_bits))
        self.assertEqual(self.output, self.gate.output_bits)

    def test_evaluate(self):
        self.gate.output_bits = [2]
        self.gate.evaluate()
        self.assertEqual(self.output, self.gate.output_bits)
