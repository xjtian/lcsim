from lcsim.components import sources

__author__ = 'Jacky'

import unittest


class TestDigitalSourceBase(unittest.TestCase):
    """
    Test for DigitalSourceBase class.
    """
    def test_constructor(self):
        gate = sources.DigitalSourceBase('Test', 1)

        self.assertEqual('Test', gate.name)
        self.assertEqual(1, gate.output_bit)
        self.assertEqual(0, len(gate._input_bits))

        # Make sure exception is raised if non-bit value is passed
        try:
            sources.DigitalSourceBase('Test', 2)
            self.fail('Digital source allowed non-bit value')
        except ValueError:
            self.assert_(True)

    def test_evaluate(self):
        gate = sources.DigitalSourceBase('Test', 1)
        # Arbitrarily modify output_bits to make sure it goes back to what
        # it should be
        gate.output_bit = 0
        gate.evaluate()
        self.assertEqual(1, gate.output_bit)


class TestDigitalZero(unittest.TestCase):
    """
    Test for DigitalZero class.
    """
    def setUp(self):
        self.gate = sources.DigitalZero()

    def test_constructor(self):
        self.assertEqual('D0', self.gate.name)
        self.assertEqual(0, len(self.gate._input_bits))
        self.assertEqual(0, self.gate.output_bit)

    def test_evaluate(self):
        self.gate.output_bit = 2
        self.gate.evaluate()
        self.assertEqual(0, self.gate.output_bit)


class TestDigitalOne(unittest.TestCase):
    """
    Test for DigitalOne class.
    """
    def setUp(self):
        self.gate = sources.DigitalOne()

    def test_constructor(self):
        self.assertEqual('D1', self.gate.name)
        self.assertEqual(0, len(self.gate._input_bits))
        self.assertEqual(1, self.gate.output_bit)

    def test_evaluate(self):
        self.gate.output_bit = 2
        self.gate.evaluate()
        self.assertEqual(1, self.gate.output_bit)
